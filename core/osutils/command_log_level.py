"""
Device type enum.
"""
from enum import Enum


class CommandLogLevel(Enum):
    SILENT = 0
    COMMAND_ONLY = 1
    FULL = 2
