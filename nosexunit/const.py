#-*- coding: utf-8 -*-
import os

# Loggers
# -------
# Nose's root logger
LOGGER = 'nose'

# Panels
# ------
# Target for right panels
PANEL_TARGET_RIGHT = 'right_panel'
# Target for left panels
PANEL_TARGET_LEFT = 'left_panel'

# Output
# ------
# HTML
HTML = 'html'
# Text
TEXT = 'text'

# Target folders
# --------------
# Root target
TARGET = os.path.join('target', 'NoseXUnit')
# Test target
TARGET_CORE = os.path.join(TARGET, 'core')
# PyLint target
TARGET_AUDIT = os.path.join(TARGET, 'audit')
# Coverage target
TARGET_COVER = os.path.join(TARGET, 'cover')

# Prefix
# ------
# Prefix for core report file
PREFIX_CORE = ''

# Extension
# ---------
# Extension for core report file
EXT_CORE = 'xml'

# Search
# ------
# Exclude following folders from search
SEARCH_EXCLUDE = ['.svn', 'CVS', ]

# Test result possibilities
# -------------------------
# Test success
TEST_SUCCESS = 0
# Test failure
TEST_FAIL = 1
# Test error
TEST_ERROR = 2
# Test Skipped
TEST_SKIP = 3
# Test deprecated
TEST_DEPRECATED = 4

# Value for unknown execution time
# --------------------------------
UNK_TIME = 0

# Value for unknown errors
# ------------------------
UNK_ERR_TYPE = 'unknown'

# Init
# ----
INIT = '__init__.py'

# default
AUDIT_DEFAULT_REPORTER = 'nosexunit'

# Pickle file
AUDIT_EXCHANGE_FILE = 'exchange.pkl'

# Entry of pickle file in context
AUDIT_EXCHANGE_ENTRY = 'NOSEXUNIT_EXCHANGE_FILE'

# Exclude from audit and cover
AUDIT_COVER_EXCLUDE = ['ez_setup', 'setup', ]

# Get default coverage output file
COVER_OUTPUT_BASE = '.coverage'
