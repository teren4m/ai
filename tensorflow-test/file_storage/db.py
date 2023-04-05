import sqlite3
from sqlite3 import Cursor, Connection
import json

metadata_table_create = '''
    CREATE TABLE IF NOT EXISTS {}_metadata (
	    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	    name TEXT NOT NULL,
	    key TEXT NOT NULL,
	    value TEXT NOT NULL
    );
    '''
metadata_table_insert = '''
    INSERT INTO {}_metadata(name, key, value) 
    VALUES(?, ?, ?)
'''


collection_table_create = '''
    CREATE TABLE IF NOT EXISTS {} (
	    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	    name TEXT NOT NULL UNIQUE,
	    path TEXT NOT NULL,
        FOREIGN KEY (name) REFERENCES metadata ON DELETE CASCADE ON UPDATE CASCADE
    );
    '''

collection_table_insert = '''
    INSERT INTO {}(name, path) 
    VALUES(?, ?)
'''
collection_table_get = '''
    SELECT *
    FROM {} AS c
'''

data_table_get = '''
    SELECT 
        c.id AS id,
        c.name AS name,
        c.path AS path,
        m.key AS key,
        m.value AS value
    FROM 
        {0} AS c
    LEFT JOIN {0}_metadata AS m 
        ON m.name = c.name
    WHERE 
        c.name = ?
    ORDER BY 
        c.id
'''

data_table_get_collection = '''
    SELECT 
        c.id AS id,
        c.name AS name,
        c.path AS path,
        m.key AS key,
        m.value AS value
    FROM 
        {0} AS c
    LEFT JOIN {0}_metadata AS m 
        ON m.name = c.name
    ORDER BY 
        c.id
'''

update_metadata = '''
    UPDATE 
        {0}_metadata
    SET 
        key = '{2}',
        value = '{3}'
    WHERE 
        name = '{1}' AND key = '{2}';
'''

select_metadata = '''
    SELECT 
        *
    FROM 
        {0}_metadata
    WHERE 
        name = '{1}' AND key = '{2}';
'''

insert_metadata = '''
    INSERT INTO {0}_metadata(name, key, value) 
    VALUES('{1}', '{2}', '{3}')
'''


def is_table_exist(cur: Cursor, name: str) -> bool:
    sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
    cur.execute(sql_query)
    return name in [item[0] for item in cur.fetchall()]


def drop_table(cur: Cursor, name: str):
    sql_query = 'DROP TABLE IF EXISTS {};'.format(name)
    cur.execute(sql_query)


class CollectionMapper:

    metadata: list[tuple]
    collection: list[tuple]

    def __init__(self) -> None:
        self.metadata = []
        self.collection = []

    def map_data(self, data: dict):
        name = data['name']
        path = data['path']
        metadata: dict = data['metadata']
        metadata_maped = [(name, key, json.dumps(
            metadata[key])) for key in metadata.keys()]
        self.collection.append((name, path))
        self.metadata.extend(metadata_maped)

    def map(self, data_list: list[dict]):
        [self.map_data(item) for item in data_list]


class DBHelper():
    db_path: str
    con: Connection
    cur: Cursor
    collection: str

    def __init__(self, db_path: str, collection: str) -> None:
        self.collection = collection
        self.db_path = db_path

    def init(self):
        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()
        self.cur.execute(metadata_table_create.format(self.collection))
        self.cur.execute(collection_table_create.format(self.collection))

    def insert(self, data_list: list[dict]):
        mapper = CollectionMapper()
        mapper.map(data_list)
        self.cur.executemany(
            metadata_table_insert.format(self.collection),
            mapper.metadata
        )
        self.cur.executemany(
            collection_table_insert.format(self.collection),
            mapper.collection
        )
        self.con.commit()

    def get(self, name: str):
        self.cur.execute(data_table_get.format(self.collection), [name])
        return self.cur.fetchall()

    def get_list(self) -> list:
        self.cur.execute(data_table_get_collection.format(self.collection))
        return self.cur.fetchall()

    def update_metadata(self, name: str, key: str, value: str):
        query = select_metadata.format(
            self.collection, name, key, value)
        self.cur.execute(query)
        x = self.cur.fetchall()
        if len(x):
            query = update_metadata.format(
                self.collection, name, key, value)
        else:
            query = insert_metadata.format(
                self.collection, name, key, value)
        
        print(query)
        self.cur.execute(query)
        self.con.commit()

    def update(self, query:str):
        self.cur.execute(query)
        self.con.commit()

    def close(self):
        self.con.close()
