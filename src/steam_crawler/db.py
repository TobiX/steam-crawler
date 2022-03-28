# SPDX-License-Identifier: MIT-0

import sqlite3
from importlib.resources import read_text
from collections import defaultdict
from collections.abc import Iterator


class Database:
    def __init__(self, file):
        self.db = sqlite3.connect(file)
        self.db.row_factory = sqlite3.Row

        cursor = self.db.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')
        cursor.executescript(read_text(__package__, 'schema.sql'))
        self.db.commit()

        columns = {}
        for table in self.db.cursor().execute('PRAGMA table_list'):
            tname = table['name']
            cols = [x['name'] for x in self.db.cursor().execute(f'PRAGMA table_info({tname})')]
            columns[tname] = cols
        self.columns = columns

    def upserter(self, table: str, data: list[dict[str, object]]):
        '''Builds and executes an UPSERT expression for a specific table.
        Expects the key to be just "appid" and a column "last_change_number" to
        exist in the table.'''
        cols = [x for x in self.columns[table] if x != 'appid']
        placeholders = ','.join(':' + x for x in cols)
        update = ','.join(x + '=excluded.' + x for x in cols)
        query = f'''INSERT INTO {table} (appid,{','.join(cols)})
            VALUES (:appid,{placeholders})
            ON CONFLICT(appid) DO UPDATE SET {update}
            WHERE excluded.last_change_number > {table}.last_change_number
        '''
        self.db.cursor().executemany(query, data)

    def update_apps(self, response):
        '''Update apps data from a get_product_info request.'''
        changes = []
        common = []
        steamdeck = []
        for appid, data in response['apps'].items():
            cnr = data['_change_number']
            changes.append(_app_dict(appid, cnr, {'sha': data['_sha'], 'size': data['_size']}))
            if 'common' in data:
                cdata = _app_dict(appid, cnr, data['common'])
                cdata.update(data.get('extended', {}))
                cdata.update(data.get('config', {}))
                common.append(cdata)
                if 'oslist' in cdata:
                    for os in cdata['oslist'].split(','):
                        cdata['os_' + os] = True
                if 'steam_deck_compatibility' in cdata:
                    deckdata = cdata['steam_deck_compatibility']
                    deckdata.update(deckdata.pop('configuration', {}))
                    steamdeck.append(_app_dict(appid, cnr, deckdata))

        self.upserter('apps_changes', changes)
        self.upserter('apps', common)
        self.upserter('apps_steamdeck', steamdeck)
        self.db.commit()

    def get_last_change(self) -> int:
        for row in self.db.cursor().execute('SELECT max(last_change_number) FROM apps_changes'):
            if row[0]:
                return int(row[0])
        return 0


def _app_dict(appid: int, change_number: int, data: dict[str, object]) -> dict[str, object]:
    ret = defaultdict(lambda: None, appid=appid, last_change_number=change_number)
    ret.update(data)
    return ret
