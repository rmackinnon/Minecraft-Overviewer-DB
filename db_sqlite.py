import sqlite3
from db_defs import *

__author__ = 'Rob MacKinnon <rob.mackinnon@gmail.com>'
__name__ = "overviewer_db.db_sqlite"
__package__ = "overviewer_db"
__copyright__ = "Copyright (c) 2016 Rob MacKinnon"
__license__ = "MIT"


def processResults(result, mapping):
    _retResults = []
    for _row in result:
        _record = {}
        for _keyIdx, _key in enumerate(mapping):
            _record.update({_key: _row[_keyIdx]})
        _retResults.append(_record)
    return _retResults


def fetchall(db, table_obj):
    table_name = table_obj["table_name"]
    _success, _result = db.cursor_execute("select * FROM ?;", table_name)
    if not _success:
        print "Failed attempt to get data from table: %s" % table_name
        return False, None
    _success, _result = db.fetchall()
    if not _success:
        print "Query failed to return data sets from table: %s" % table_name
        return False, None
    _returnList = []
    for _player in _result:
        _returnDict = {}
        for _idx, _col in enumerate(table_obj["columns"]):
            _returnDict.update(map(_col["name"], _result[_idx]))
        _returnList.append(_returnDict)
    return True, _returnList


def fetchone(db, table_obj, fieldname, value):
    table_name = table_obj["table_name"]
    _success, _result = db.cursor_execute("SELECT * FROM ? WHERE ?='?';", (table_name, fieldname, value))
    if not _success:
        print "Failed attempt to get table: %s; %s=%s" % (table_name, fieldname, value)
        return False, None
    _success, _result = db.fetchone()
    if not _success:
        print "Query failed to return from table: %s; %s=%s" % (table_name, fieldname, value)
        return False, None
    _returnDict = {}
    for _idx, _col in enumerate(table_obj["columns"]):
        _returnDict.update(map(_col["name"], _result[_idx]))
    return True, [_returnDict]


class SQLiteDB(object):
    src_file = None
    conn = None
    cursor = None

    def __init__(self, fileName):
        self.src_file = fileName
        try:
            self.conn = sqlite3.connect(self.src_file, check_same_thread=True)
        # self.conn = sqlite3.connect(self.src_file)
        except sqlite3.OperationalError as e:
            print "!!! Problem opening database file, please check the configuration file."
            exit(1)
        self.cursor = self.conn.cursor()
        if not self.checkTableExists('overviewer'):
            # Database doesn't exist
            print "+++ Setting up database for first run ..."
            self.setup()
            self.commit()
            self.close()
            print "... Re-opening configured database ..."
            self.conn = sqlite3.connect(self.src_file)
            self.cursor = self.conn.cursor()

    def checkTableExists(self, table_name):
        _success, _result = self.cursor_execute(r"SELECT 1 FROM sqlite_master WHERE type='table' AND name=?;",
                                                [table_name])
        if not _success:
            print "!!! Unable to perform a table exists check."
            exit(1)
        _result = self.cursor.fetchall()
        return len(_result) > 0

    def close(self):
        self.conn.close()

    def setup(self):
        _success, _result = self.execute("PRAGMA foreign_keys = ON;")
        if not _success:
            print "Unable to enable foreign key support."
            raise Exception

        for _table in [TABLE_OVERVIEWER, TABLE_POI_CLASSTYPE, TABLE_WORLD_DATA]:
            _columns = []
            for _col in _table.columns:
                _colText = "{NAME} {TYPE}".format(NAME=_col["name"], TYPE=_col["type"])
                if _col["is_Unique"]:
                    _colText += " UNIQUE"
                if not _col["is_Nullable"]:
                    _colText += " NOT NULL"
                _columns.append(_colText)

            _PK_str = ""
            _UQ_str = ""
            _FK_str = ""

            if _table.primary_key is not None:
                _PK_str = ", PRIMARY KEY({PK} {PK_ORDER})".format(
                    PK=_table.primary_key["column"],
                    PK_ORDER=_table.primary_key["order"]
                )

            if _table.unique is not None:
                _UQ = []
                for _unique in _table.unique:
                    _str = "UNIQUE({FIELDS})".format(FIELDS=", ".join(_unique["columns"]))
                    if "onConflict" in _unique:
                        _str += " ON CONFLICT {RESOLUTION}".format(RESOLUTION=_unique["onConflict"])
                    _UQ.append(_str)
                if len(_UQ) > 0:
                    _UQ_str = ", "+", ".join(_UQ)

            if _table.foreign_key is not None:
                _FK = []
                for _key in _table.foreign_key:
                    _FK.append("FOREIGN KEY(%s) REFERENCES %s(%s)" % (
                        ",".join(_key["columns"]),
                        _key["ref"]["table"],
                        ",".join(_key["ref"]["columns"])
                    ))
                if len(_FK) > 0:
                    _FK_str = ", "+", ".join(_FK)

            _sql = "CREATE TABLE IF NOT EXISTS {TABLE_NAME}({COLUMNS}{PK}{UQ}{FK});".format(
                TABLE_NAME=_table.table_name,
                COLUMNS=", ".join(_columns),
                PK=_PK_str,
                UQ=_UQ_str,
                FK=_FK_str
               )
            _success, _table_result = self.execute(_sql)
            if not _success:
                print "Unable to create default table: %s" % _table.table_name
                exit()

            # We need to see if there is default data being set or not.  If so, load it into the table...
            if _table.default_data is not None:
                _success, _table_result = self.insert(_table,
                                                      _table.default_data["fields"],
                                                      _table.default_data["values"])
                if not _success:
                    self.rollback()
                    self.close()
                    print "Unable to insert default data into table: %s" % _table.table_name
                    exit()
                self.commit()

    def execute(self, statement, replacements=None):
        try:
            if replacements is None:
                return True, self.conn.execute(statement)
            return True, self.conn.execute(statement, replacements)
        except Exception, e:
            print e
            return False, None

    def executemany(self, statement, replacements=None):
        try:
            if replacements is None:
                return True, self.conn.executemany(statement)
            return True, self.conn.executemany(statement, replacements)
        except Exception, e:
            print e
            return False, None

    def commit(self):
        try:
            return True, self.conn.commit()
        except Exception, e:
            print e
            return False, None

    def rollback(self):
        try:
            return True, self.conn.rollback()
        except Exception, e:
            print e
            return False, None

    def cursor_execute(self, statement, replacements=None):
        try:
            if replacements is None:
                return True, self.cursor.execute(statement)
            return True, self.cursor.execute(statement, replacements)
        except Exception, e:
            print e
            return False, None

    def cursor_executemany(self, statement, replacements=None):
        try:
            if replacements is None:
                return True, self.cursor.executemany(statement)
            return True, self.cursor.executemany(statement, replacements)
        except Exception, e:
            print e
            return False, None

    def fetchone(self, statement):
        try:
            return True, self.cursor.fetchone(statement)
        except Exception, e:
            print e
            return False, None

    def fetchall(self, statement, replacements=None):
        try:
            self.cursor_execute(statement, replacements)
            return True, self.cursor.fetchall()
        except Exception, e:
            print e
            return False, None

    def fetchmany(self, sz=1024):
        try:
            return True, self.cursor.fetchmany(size=sz)
        except Exception, e:
            print e
            return False, None

    def insert(self, table, fields, values):

        _sql = 'INSERT INTO {TABLE} ({FIELDS}) VALUES ({VALUES});'.format(TABLE=table.table_name,
                                                                          FIELDS=', '.join(fields),
                                                                          VALUES=', '.join(['?']*len(fields)))

        return self.cursor_executemany(_sql, values)
