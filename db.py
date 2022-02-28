
import sqlite3
from operator import itemgetter


class Database:
    CREATE_APPS = '''CREATE TABLE IF NOT EXISTS apps (
        appid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        last_modified INTEGER NOT NULL,
        price_change_number INTEGER NOT NULL
    )'''

    def __init__(self):
        self.db = sqlite3.connect('steam.db')

        cursor = self.db.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')
        self.db.commit()
        cursor.execute(self.CREATE_APPS)
        cursor.execute('CREATE INDEX IF NOT EXISTS apps_last_mod ON apps(last_modified)')
        self.db.commit()

    def update_apps(self, response):
        '''Update apps data from a IStoreService.GetAppList webapi request.'''
        cursor = self.db.cursor()
        cursor.executemany('''INSERT INTO apps (appid, name, last_modified, price_change_number)
            VALUES (:appid, :name, :last_modified, :price_change_number)
            ON CONFLICT(appid) DO UPDATE SET name=excluded.name,
              last_modified=excluded.last_modified, price_change_number=excluded.price_change_number
            WHERE excluded.last_modified > apps.last_modified
            ''',
            response['apps'])
        self.db.commit()

    def latest_app_update(self):
        cursor = self.db.cursor()
        cursor.execute('select max(last_modified) from apps')
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

