"""
Type of `tns prepare` enumeration.
"""
from enum import Enum


class Prepare(Enum):
    SKIP = 0  # Prepare is skipped at all (no files changed).
    INCREMENTAL = 1  # Some js/xml/css file is changed and incremental prepare is triggered.
    FULL = 2  # Full prepare. Rebuild native frameworks.
    FIRST_TIME = 3  # When platforms are not added to project they should be added and then FULL prepare is executed.
