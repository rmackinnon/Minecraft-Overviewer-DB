import ConfigParser

__author__ = 'Rob MacKinnon <rob.mackinnon@gmail.com>'
__name__ = "overviewer_db.config"
__package__ = "overviewer_db"
__copyright__ = "Copyright (c) 2016 Rob MacKinnon"
__license__ = "MIT"

CONFIG = None
DB_FILE = None
DB = None


def readConfigFile(conf=None):
    globals()["CONFIG"] = ConfigParser.ConfigParser()
    if conf is None:
        print("    Using default configuration files")
        globals()["CONFIG"].read(['server.conf', '../overviewer.conf'])
    else:
        print("+++ Using configuration file: %s") % conf
        globals()["CONFIG"].read([conf])
    globals()["DB_FILE"] = globals()["CONFIG"].get("db", "source")
    # print("Using database file: %s") % globals()["DB_FILE"]


def getConfigSetting(section, setting):
    try:
        _confOpt = CONFIG.get(section, setting)
    except AttributeError as e:
        print("!!! Unable to open the configuration file.")
        print e
        exit(1)
    return _confOpt
