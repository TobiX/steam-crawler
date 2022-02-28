#!/usr/bin/env python3

import keyring
from steam import webapi

from db import Database

key = keyring.get_password('steam', 'key')
if not key or len(key) != 32:
    raise RuntimeError("Invalid API key!")

db = Database()
api = webapi.WebAPI(key)

params = {}
after = db.latest_app_update()
if after:
    params['if_modified_since'] = after
have_more_results = True
while have_more_results:
    apps = api.IStoreService.GetAppList(**params)['response']
    db.update_apps(apps)
    have_more_results = apps.get('have_more_results', False)
    if have_more_results:
        params['last_appid'] = apps['last_appid']
