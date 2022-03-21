# SPDX-License-Identifier: MIT-0

from .crawler import Updater


def run():
    Updater('steam.db').run()
