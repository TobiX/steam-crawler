# SPDX-License-Identifier: MIT-0
from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from time import sleep

from rich.progress import MofNCompleteColumn, Progress
from steam.client import SteamClient
from steam.webapi import WebAPI

from .db import Database


def grouper(orig, n: int):
    work = list(orig)
    for i in range(0, len(work), n):
        yield work[i:i + n]


@contextmanager
def anon_client():
    s = SteamClient()
    s.anonymous_login()
    yield s
    s.disconnect()


class Updater:
    def __init__(self, db: Database):
        self.db = db

    def run(self):
        last_change = self.db.get_last_change()
        print(f'Last change: {last_change}')
        with anon_client() as client:
            changes = client.get_changes_since(last_change, True, False)
            if changes.force_full_update or changes.force_full_app_update:
                print('Full update forced.')
                resp = WebAPI(None).ISteamApps.GetAppList_v2()
                apps = (x['appid'] for x in resp['applist']['apps'])
            else:
                apps = (entry.appid for entry in changes.app_changes)
            self.update_apps(client, apps)
        last_change = self.db.get_last_change()
        print(f'New last change: {last_change}')

    def update_apps(self, client, apps: Iterator[int]):
        aset = set(apps)
        with Progress(*Progress.get_default_columns(),
                      MofNCompleteColumn()) as progress:
            down = progress.add_task('[red]Download', total=len(aset))
            commit = progress.add_task('[green]Process', total=len(aset))

            for part in grouper(aset, 1000):
                progress.update(down, advance=len(part))
                data = client.get_product_info(apps=list(part))
                progress.update(commit, advance=len(part))
                self.db.update_apps(data)
                if len(part) == 1000:
                    sleep(1)
