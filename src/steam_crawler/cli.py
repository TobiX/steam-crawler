# SPDX-License-Identifier: MIT-0
from __future__ import annotations

from .crawler import Updater


def run():
    Updater('steam.db').run()
