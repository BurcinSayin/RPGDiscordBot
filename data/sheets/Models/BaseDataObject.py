class BaseDataObject:
    def __init__(self, index, obj_data):
        self._index = index
        self._original_data = obj_data
        # Clone of original data
        self._current_data = obj_data[:]
        self._is_deleted = False

    @property
    def id(self) -> int:
        return int(self._current_data[0])

    def delete_me(self):
        self._is_deleted = True

    def is_deleted(self):
        return self._is_deleted

    def get_changes(self):
        ret_val = []
        if self._is_deleted:
            ret_val.append([self._index, -1, "***DELETED***"])
        else:
            array_size = len(self._original_data)
            for i in range(1, array_size):
                if self._original_data[i] != self._current_data[i] or self._index == 0:
                    ret_val.append([self._index, i+1, self._current_data[i]])
        return ret_val
