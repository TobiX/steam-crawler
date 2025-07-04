# SPDX-License-Identifier: MIT-0
from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__package__)
except PackageNotFoundError:
    # package is not installed
    pass
