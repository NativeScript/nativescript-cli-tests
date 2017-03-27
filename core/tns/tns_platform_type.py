"""
Platforms enumeration.
"""
from enum import Enum


class Platform(Enum):
    NONE = 0  # No platform
    ANDROID = 1  # Only Android platform
    IOS = 2  # Only iOS platform
    BOTH = 3  # Both platforms
