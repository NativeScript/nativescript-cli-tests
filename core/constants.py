'''
Created on Dec 14, 2015

This file contains only constants.

TODO: Separate as a config file.

@author: vchimev
'''

import os


TNS_PATH = os.path.join('node_modules', '.bin', 'tns')

# 180 seconds are not enough for not accelerated emulators
DEFAULT_TIMEOUT = 300 # seconds
