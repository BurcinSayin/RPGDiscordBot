from dataclasses import asdict


class BaseData:

    def __init__(self, db, table_name, key_name, key_type):
        self._db = db
        self._table_name = table_name
        self.key_attribute_name = key_name
        self.key_attribute_type = key_type

        tables = list(map(lambda a: a.name, db.tables.all()))
        if table_name in tables:
            self.table = self._db.Table(self._table_name)
        else:
            self.table = self.create_table()

    def create_table(self):
        created_table = self._db.create_table(
            TableName=self._table_name,
            KeySchema=self.get_key_schema(),
            AttributeDefinitions=self.get_attribute_defs(),
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        created_table.wait_until_exists()
        return created_table

    def get_key_schema(self):
        return [
            {
                'AttributeName': self.key_attribute_name,
                'KeyType': 'HASH'
            }
        ]

    def get_attribute_defs(self):
        base_attributes = [
            {
                'AttributeName': self.key_attribute_name,
                'AttributeType': self.key_attribute_type
            }
        ]
        return base_attributes

    def save_data_obj(self, data_obj):
        ret_val = data_obj
        save_data = asdict(data_obj)
        self.table.put_item(
            Item=save_data
        )
        return data_obj

