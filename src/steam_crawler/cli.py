# SPDX-FileCopyrightText: © Tobias Gruetzmacher <tobias-git@23.gs>
# SPDX-License-Identifier: MIT-0
from __future__ import annotations

import argparse
import pathlib

from .db import Database
from .crawler import Updater


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', type=pathlib.Path,
        default='steam.db', help='the database file to use')

    args = parser.parse_args()

    db = Database(args.database)
    Updater(db).run()
