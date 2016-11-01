"""
Settings
"""
import os
import platform


class OSType(object):
    WINDOWS = 0
    LINUX = 1
    OSX = 2


class DeviceType(object):
    ANDROID = 0
    IOS = 1
    EMULATOR = 2
    SIMULATOR = 3


# Timeout settings (in seconds)
COMMAND_TIMEOUT = 600

# Current OS
CURRENT_OS = OSType.LINUX
if "Windows" in platform.platform():
    CURRENT_OS = OSType.WINDOWS
if "Darwin" in platform.platform():
    CURRENT_OS = OSType.OSX

# Test run type
TEST_RUN = os.environ.get("TEST_RUN")
TEST_RUN_HOME = os.getcwd()

# Test packages location
CLI_PATH = os.environ["CLI_PATH"]
ANDROID_PATH = os.environ["ANDROID_PATH"]
TNS_MODULES_PATH = os.environ["TNS_MODULES_PATH"]
TNS_MODULES_WIDGETS_PATH = os.environ["TNS_MODULES_WIDGETS_PATH"]
if "IOS_PATH" in os.environ:
    IOS_PATH = os.environ["IOS_PATH"]
    IOS_INSPECTOR_PATH = os.environ["IOS_INSPECTOR_PATH"]
else:
    IOS_PATH = None
    IOS_INSPECTOR_PATH = None

# Local packages path
TNS_PATH = os.path.join("node_modules", ".bin", "tns")
SUT_ROOT_FOLDER = TEST_RUN_HOME + os.path.sep + "sut"
ANDROID_RUNTIME_PATH = os.path.join(SUT_ROOT_FOLDER, "tns-android.tgz")
ANDROID_RUNTIME_SYMLINK_PATH = os.path.join(SUT_ROOT_FOLDER, "tns-android", "package")
IOS_RUNTIME_PATH = os.path.join(SUT_ROOT_FOLDER, "tns-ios.tgz")
IOS_RUNTIME_SYMLINK_PATH = os.path.join(SUT_ROOT_FOLDER, "tns-ios", "package")
IOS_INSPECTOR_PACKAGE = os.path.join(SUT_ROOT_FOLDER, "tns-ios-inspector.tgz")

# Output settigns
OUTPUT_FOLDER = TEST_RUN_HOME + os.path.sep + "out"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, 'output.txt')
TEST_LOG = os.path.join(OUTPUT_FOLDER, 'testLog.txt')
VERBOSE_LOG = os.path.join(OUTPUT_FOLDER, 'verboseLog.txt')

# Default Simulator and Emulator
EMULATOR_NAME = "Emulator-Api19-Default"
SIMULATOR_NAME = "iPhone691"

# Android SDK
ADB_PATH = os.path.join(os.environ.get("ANDROID_HOME"), "platform-tools", "adb")
EMULATOR_PATH = os.path.join(os.environ.get('ANDROID_HOME'), 'tools', 'emulator')

# Android Build Settings
ANDROID_KEYSTORE_PATH = os.environ.get("ANDROID_KEYSTORE_PATH")
ANDROID_KEYSTORE_PASS = os.environ.get("ANDROID_KEYSTORE_PASS")
ANDROID_KEYSTORE_ALIAS = os.environ.get("ANDROID_KEYSTORE_ALIAS")
ANDROID_KEYSTORE_ALIAS_PASS = os.environ.get("ANDROID_KEYSTORE_ALIAS_PASS")

# iOS Build Settings
DEVELOPMENT_TEAM = os.environ.get("DEVELOPMENT_TEAM")

# Unknown
DEBUG = 0
