from copy import deepcopy

__author__ = 'Rob MacKinnon <rob.mackinnon@gmail.com>'
__name__ = "overviewer_db.db_classes"
__package__ = "overviewer_db"
__copyright__ = "Copyright (c) 2016 Rob MacKinnon"
__license__ = "MIT"


class TableReference:
    table_name = ""
    columns_list = []
    columns_insert_ignore = []
    columns = []
    primary_key = None
    unique = None
    foreign_key = None
    default_data = None

    def __init__(self, table, pk=None):
        self.table_name = table
        self.primary_key = pk
        self.columns = []

    def add_columns(self, column_list):
        _local_list = []
        _local_cols = []
        for _column in column_list:
            _local_list.append(_column["name"])
            _local_cols.append(_column)
        self.columns_list = _local_list
        self.columns = _local_cols

    def on_insert_ignore(self, column_list):
        self.columns_insert_ignore = column_list

    def set_default_dataset(self, fields, values):
        self.default_data = {"fields": fields, "values": values}

    def get_insert_cols(self):
        _active_list = deepcopy(self.columns_list)
        for _rem in self.columns_insert_ignore:
            if _rem in _active_list:
                _active_list.remove(_rem)
        return _active_list

    def get_custom_select_cols(self, include_fields=None, exclude_fields=None):
        _active_list = deepcopy(self.columns_list)
        if exclude_fields is not None:
            for _rem in exclude_fields:
                if _rem in _active_list:
                    _active_list.remove(_rem)
        if include_fields is not None:
            _active_list.extend(include_fields)
        return _active_list

    def get_empty_record(self):
        _record = {}
        _active_list = self.get_insert_cols()
        for _f in _active_list:
            _record.update({_f: None})
        return _record
