from db_classes import TableReference

__author__ = 'Rob MacKinnon <rob.mackinnon@gmail.com>'
__name__ = "overviewer_db.db_defs"
__package__ = "overviewer_db"
__copyright__ = "Copyright (c) 2016 Rob MacKinnon"
__license__ = "MIT"

WORLD_NETHER = -1
WORLD_OVERWORLD = 0
WORLD_END = 1

POI_STATE_UNDISCOVERED = -1
POI_STATE_DISCOVERED = 0
POI_STATE_CLEARED = 1

"""
Tables Schema: poi_types
========================
id: primary key, auto-incrementing
value: Text value for field
"""
TABLE_POI_CLASSTYPE = TableReference(table="poi_class_types", pk={"column": "id", "order": "ASC"})
TABLE_POI_CLASSTYPE.add_columns([
    {"name": "id", "type": "INTEGER", "is_Nullable": True, "is_Unique": False},
    {"name": "class", "type": "TEXT", "is_Nullable": False, "is_Unique": False},
    {"name": "subclass", "type": "TEXT", "is_Nullable": False, "is_Unique": False}
])
TABLE_POI_CLASSTYPE.on_insert_ignore(["id"])
TABLE_POI_CLASSTYPE.unique = [{"columns": ["class", "subclass"], "onConflict": "FAIL"}]
TABLE_POI_CLASSTYPE.set_default_dataset(["class", "subclass"], [
    # Locations
    ('Location', 'Shelter'),
    ('Location', 'Portal'),
    ('Location', 'Mineshaft'),
    ('Location', 'Village'),
    ('Location', 'Town'),
    ('Location', 'City'),
    ('Location', 'Well'),
    ('Location', 'Monument_Ocean'),
    ('Location', 'Temple_Desert'),
    ('Location', 'Temple_Jungle'),
    ('Location', 'Witch_Hut'),
    ('Location', 'Stronghold'),
    ('Location', 'Fortress'),
    ('Location', 'Custom'),
    # TrackedObject, the following use a UUID for identity
    ('TrackedObject', 'Boat'),
    ('TrackedObject', 'Player'),
    ('TrackedObject', 'MinecartChest'),
    ('TrackedObject', 'Custom'),
    # StaticObject, static non-moving objects identified by their position
    ('StaticObject', 'MobSpawner'),
    ('StaticObject', 'Chest'),
    ('StaticObject', 'Custom'),
    # Custom Type, this is for future customization
    ('Custom', 'Custom')  # Enables usage of customJSON object
])

"""
Tables Schema: world_data
=========================
id: primary key, auto-incrementing
seed: World Seed ID
world: 0 (world), -1 (nether), 1 (end)
class_type_id: Referenced id of Class.Type pair
x: Positional integer
y: Positional integer
z: Positional integer
name: Short name or Player Name
uuid: TrackedObject uuid, or Player UUID
commonName: Caption name
desc: Long description of
state: -1 (undiscovered), 0 (discovered), 1 (cleared)
safe: 0-5, how safe is it? 5=Safe, 0=Not so much
discoveredBy: UUID of player name who discovered it.  Valid only for Location.*
clearedBy: UUID of player that marked this location cleared
partnerChestId: ID of neighboring chest. Only valid for StaticObject.Chest
spawnsEntityId: EntityId of spawned mobs.  Only valid for StaticObject.MobSpawner
"""
TABLE_WORLD_DATA = TableReference(table="world_data", pk={"column": "id", "order": "ASC"})
TABLE_WORLD_DATA.add_columns([
    {"name": "id", "type": "INTEGER", "is_Nullable": True, "is_Unique": False},
    {"name": "seed", "type": "INT", "is_Nullable": False, "is_Unique": False},
    {"name": "world", "type": "INT", "is_Nullable": False, "is_Unique": False},
    {"name": "class_type_id", "type": "TEXT", "is_Nullable": False, "is_Unique": False},
    {"name": "x", "type": "INT", "is_Nullable": False, "is_Unique": False},
    {"name": "y", "type": "INT", "is_Nullable": False, "is_Unique": False},
    {"name": "z", "type": "INT", "is_Nullable": False, "is_Unique": False},
    {"name": "name", "type": "TEXT", "is_Nullable": False, "is_Unique": False},
    {"name": "uuid", "type": "TEXT", "is_Nullable": True, "is_Unique": False},  # UUIDLeast + UUIDMost
    {"name": "commonName", "type": "TEXT", "is_Nullable": True, "is_Unique": False},
    {"name": "description", "type": "TEXT", "is_Nullable": True, "is_Unique": False},
    {"name": "state", "type": "INT", "is_Nullable": False, "is_Unique": False},
    {"name": "safe", "type": "NUMERIC", "is_Nullable": True, "is_Unique": False},
    {"name": "discoveredBy", "type": "TEXT", "is_Nullable": True, "is_Unique": False},
    {"name": "clearedBy", "type": "TEXT", "is_Nullable": True, "is_Unique": False},
    {"name": "notVisibleToPlayers", "type": "BOOLEAN", "is_Nullable": True, "is_Unique": False},
    {"name": "partnerChestId", "type": "INT", "is_Nullable": True, "is_Unique": False},
    {"name": "spawnsEntityId", "type": "TEXT", "is_Nullable": True, "is_Unique": False},
    {"name": "customJSON", "type": "BLOB", "is_Nullable": True, "is_Unique": False},
])
TABLE_WORLD_DATA.on_insert_ignore(["id"])
TABLE_WORLD_DATA.unique = [{"columns": ["class_type_id", "name", "uuid", "commonName"], "onConflict": "IGNORE"}]
TABLE_WORLD_DATA.foreign_key = [
    {"columns": ["class_type_id"], "ref": {"table": "poi_class_types", "columns": ["id"]}}
]

"""
Table Schema: overviewer
========================
setting: primary key, unique, setting name
value: value of setting
"""
TABLE_OVERVIEWER = TableReference(table="overviewer", pk={"column": "setting", "order": "ASC"})
TABLE_OVERVIEWER.add_columns([
    {"name": "setting", "type": "TEXT", "is_Nullable": False, "is_Unique": True},
    {"name": "value", "type": "BLOB", "is_Nullable": False, "is_Unique": False}
    ])
