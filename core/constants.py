'''
Created on Dec 14, 2015

This file contains all the constants.

TODO: Separate as a config file.

@author: vchimev
'''


import os


TNS_PATH = os.path.join('node_modules', '.bin', 'tns')
IOS_RUNTIME_PATH = 'tns-ios.tgz'
ANDROID_RUNTIME_PATH = 'tns-android.tgz'
IOS_RUNTIME_SYMLINK_PATH = os.path.join('tns-ios', 'package')
ANDROID_RUNTIME_SYMLINK_PATH = os.path.join('tns-android', 'package')

ADB_PATH = os.path.join(os.environ.get('ANDROID_HOME'), 'platform-tools', 'adb')

DEFAULT_OUTPUT_FILE = 'output.txt'
DEFAULT_COMMANDS_FILE = 'commands.txt'

# TODO: RESULTS_DIR = os.path.join(MAIN_DIR, 'results')

# 180 seconds are not enough for not accelerated emulators
DEFAULT_TIMEOUT = 300 # seconds
DEBUG = 0

# TODO: consider these ...
# ANDROID_KEYSTORE_PATH = os.environ.get('ANDROID_KEYSTORE_PATH')
# ANDROID_KEYSTORE_PASS = os.environ.get('ANDROID_KEYSTORE_PASS')
# ANDROID_KEYSTORE_ALIAS = os.environ.get('ANDROID_KEYSTORE_ALIAS')
# ANDROID_KEYSTORE_ALIAS_PASS = os.environ.get('ANDROID_KEYSTORE_ALIAS_PASS')

# class Enums(object):
#
#     class Language(object):
#         JavaScript = "javascript"
#         TypeScript = "typescript"
#
#     class Platform(object):
#         Android = 'android'
#         iOS = 'ios'
