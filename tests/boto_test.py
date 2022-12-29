import boto3


def list_tables():
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    tables = list(map(lambda a: a.name, dynamodb.tables.all()))
    print(tables)


if __name__ == '__main__':
    list_tables()
