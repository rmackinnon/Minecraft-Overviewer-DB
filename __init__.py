import db_sqlite
from db_defs import TABLE_OVERVIEWER
import config

__author__ = 'Rob MacKinnon <rob.mackinnon@gmail.com>'
__name__ = "overviewer_db"
__package__ = "overviewer_db"
__copyright__ = "Copyright (c) 2016 Rob MacKinnon"
__license__ = "MIT"

if __name__ == "__main__":
    print "This module cannot be run directly."
    exit(0)


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

    def add_columns(self, column_list):
        for _column in column_list:
            self.columns_list.append(_column["name"])
            self.columns.append(_column)

    def on_insert_ignore(self, column_list):
        self.columns_insert_ignore = column_list

    def set_default_dataset(self, fields, values):
        self.default_data = {"fields": fields, "values": values}



"""
Usage: Load the config, and call `load_db()` to initiate a connection to the database from your application.
"""

CONFIG_SECTION = "db"


def load_db():
    print("+++ Loading database: %s") % config.DB_FILE
    config.DB = db_sqlite.SQLiteDB(config.DB_FILE)


def updateSetting(setting, value):
    pass


def getSetting(setting):
    return db_sqlite.fetchone(config.DB, TABLE_OVERVIEWER, setting, "%")
