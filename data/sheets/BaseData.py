from gspread import Worksheet

from data.sheets.Models.BaseDataObject import BaseDataObject


class BaseData:

    def __init__(self, spreadsheet, worksheet_name):
        """

        :type spreadsheet: gspread.models.Spreadsheet
        """
        self._main_document = spreadsheet
        self.worksheet = self._main_document.worksheet(worksheet_name)
        self.subsheets = {}

    def add_sub_sheet(self, worksheet_name, ref_column_index):
        self.subsheets[worksheet_name] = {
            "sheet": self._main_document.worksheet(worksheet_name),
            "col_ref": ref_column_index
        }

    def get_sub_sheet_or_default(self, sub_sheet_name):
        sub_sheet_info = self.subsheets.get(sub_sheet_name)
        if sub_sheet_info is None:
            return None, None
        return sub_sheet_info.get("sheet"), sub_sheet_info.get("col_ref")

    def get_all(self):
        return self.worksheet.get_all_records()

    def get_last_id(self, target_sheet: Worksheet = None):
        if target_sheet is None:
            target_sheet = self.worksheet
        id_list = target_sheet.col_values(1)
        row_count = len(id_list)
        id_list.remove("id")
        return {"row_count": row_count, "last_id": int(max(id_list))}

    def insert_row(self, values, target_sheet: Worksheet = None):
        if target_sheet is None:
            target_sheet = self.worksheet
        id_data = self.get_last_id(target_sheet)
        new_row_index = id_data["row_count"] + 1
        new_row_id = id_data["last_id"] + 1
        target_sheet.update_cell(new_row_index, 1, new_row_id)
        last_col = 1
        for data in values:
            last_col += 1
            target_sheet.update_cell(new_row_index, last_col, data)

        return new_row_index, new_row_id

    def get_with_id(self, data_id, target_sheet: Worksheet = None):
        if target_sheet is None:
            target_sheet = self.worksheet
        data_index = self.find_in_column(1, data_id, target_sheet)
        return self.get_data_from_index(data_index)

    def get_data_from_index(self, index, target_sheet: Worksheet = None):
        ret_val = None
        if target_sheet is None:
            target_sheet = self.worksheet
        header_list = target_sheet.row_values(1)
        if index > 0:
            char_data = target_sheet.row_values(index)
            ret_val = dict(zip(header_list, char_data))
        return ret_val

    def find_in_column(self, column_no, to_find, target_sheet: Worksheet = None):
        ret_val = -1
        if target_sheet is None:
            target_sheet = self.worksheet
        found_cell = target_sheet.find(to_find, None, column_no)

        if found_cell is not None:
            ret_val = found_cell.row

        # values_list = self.worksheet.col_values(column_no)
        # try:
        #     ret_val = values_list.index(str(to_find)) + 1
        # except Exception as e:
        #     ret_val = -1

        return ret_val

    def get_data_obj(self, class_ref, obj_index, target_sheet: Worksheet = None) -> BaseDataObject:
        if target_sheet is None:
            target_sheet = self.worksheet
        if obj_index > 0:
            obj_data = target_sheet.row_values(obj_index)
            return class_ref(obj_index, obj_data)
        else:
            return None

    def get_sub_data_obj_list(self, worksheet_name, class_ref, ref_data) -> list[BaseDataObject]:
        ret_val = []
        # sub_sheet_info = self.subsheets.get(worksheet_name)
        # if sub_sheet_info is None:
        #     return ret_val
        # sub_sheet = sub_sheet_info.get("sheet")
        # col_ref = sub_sheet_info.get("col_ref")
        sub_sheet, col_ref = self.get_sub_sheet_or_default(worksheet_name)
        if sub_sheet is None:
            return ret_val
        found_refs = sub_sheet.findall(ref_data, None, col_ref)
        for sub_data_cell in found_refs:
            to_add = self.get_data_obj(class_ref, sub_data_cell.row, sub_sheet)
            if to_add is not None:
                ret_val.append(to_add)
        return ret_val

    def save_simple_data_obj(self, data_obj: BaseDataObject, target_sheet: Worksheet = None):
        changes = data_obj.get_changes()
        if target_sheet is None:
            target_sheet = self.worksheet
        delete_list = []
        insert_row_data = []
        # Do Updates First
        for row_index, col_index, changed_data in changes:
            if col_index > 0:
                if row_index > 0:
                    target_sheet.update_cell(row_index, col_index, changed_data)
                else:
                    insert_row_data.append(changed_data)
            else:
                delete_list.append(row_index)
        # Do delete Second
        if len(delete_list) > 0:
            for deleted_index in delete_list:
                target_sheet.delete_rows(deleted_index)
        # Insert Last
        if len(insert_row_data) > 0:
            self.insert_row(insert_row_data, target_sheet)

    def save_data_obj(self, data_obj: BaseDataObject, target_sheet: Worksheet = None):
        if target_sheet is None:
            target_sheet = self.worksheet
        self.save_simple_data_obj(data_obj, target_sheet)
