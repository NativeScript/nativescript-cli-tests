"""
Device types enumeration.
"""
from enum import Enum


class DeviceType(Enum):
    ANDROID = 0
    IOS = 1
    EMULATOR = 2
    SIMULATOR = 3
