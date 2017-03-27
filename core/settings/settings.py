"""
Settings
"""
import os
import platform

from core.osutils.os_type import OSType

COMMAND_TIMEOUT = 600  # Timeout settings (in seconds).

# Current OS
CURRENT_OS = OSType.LINUX
if "Windows" in platform.platform():
    CURRENT_OS = OSType.WINDOWS
if "Darwin" in platform.platform():
    CURRENT_OS = OSType.OSX

TEST_RUN_HOME = os.getcwd()  # Get test run root folder.

# Test packages location from env. variables
BASE_PACKAGE_PATH = os.environ.get("BASE_PACKAGE_PATH", "/tns-dist")
BRANCH = os.environ.get("BRANCH", "master").lower()
SHARE_BRANCH = BRANCH
if "release" in BRANCH:
    SHARE_BRANCH = "Release"
else:
    SHARE_BRANCH = "Stable"
SHARE_BRANCH = os.environ.get("SHARE_BRANCH", SHARE_BRANCH)

# Set source location of separate package based on base path
CLI_PATH = os.environ.get("CLI_PATH", os.path.join(BASE_PACKAGE_PATH, "CLI", SHARE_BRANCH, "nativescript.tgz"))
ANDROID_PATH = os.environ.get("ANDROID_PATH",
                              os.path.join(BASE_PACKAGE_PATH, "tns-android", SHARE_BRANCH, "tns-android.tgz"))
IOS_PATH = os.environ.get("IOS_PATH", os.path.join(BASE_PACKAGE_PATH, "tns-ios", SHARE_BRANCH, "tns-ios.tgz"))
TNS_MODULES_PATH = os.environ.get("TNS_MODULES_PATH",
                                  os.path.join(BASE_PACKAGE_PATH, "tns-modules", SHARE_BRANCH, "tns-core-modules.tgz"))
TNS_MODULES_WIDGETS_PATH = os.environ.get("TNS_MODULES_WIDGETS_PATH",
                                          os.path.join(BASE_PACKAGE_PATH, "android-widgets", SHARE_BRANCH,
                                                       "tns-core-modules-widgets.tgz"))
TNS_PLATFORM_DECLARATIONS_PATH = os.environ.get("TNS_PLATFORM_DECLARATIONS_PATH",
                                                os.path.join(BASE_PACKAGE_PATH, "tns-modules", SHARE_BRANCH,
                                                             "tns-platform-declarations.tgz"))
IOS_INSPECTOR_PATH = os.environ.get("IOS_INSPECTOR_PATH",
                                    os.path.join(BASE_PACKAGE_PATH, "tns-ios-inspector", SHARE_BRANCH,
                                                 "tns-ios-inspector.tgz"))

# Set local location of test packages
TNS_PATH = os.path.join("node_modules", ".bin", "tns")
SUT_ROOT_FOLDER = TEST_RUN_HOME + os.path.sep + "sut"
ANDROID_RUNTIME_PATH = os.path.join(SUT_ROOT_FOLDER, "tns-android.tgz")
ANDROID_RUNTIME_SYMLINK_PATH = os.path.join(SUT_ROOT_FOLDER, "tns-android", "package")
IOS_RUNTIME_PATH = os.path.join(SUT_ROOT_FOLDER, "tns-ios.tgz")
IOS_RUNTIME_SYMLINK_PATH = os.path.join(SUT_ROOT_FOLDER, "tns-ios", "package")
IOS_INSPECTOR_PACKAGE = os.path.join(SUT_ROOT_FOLDER, "tns-ios-inspector.tgz")

# Output settings
OUTPUT_FOLDER = TEST_RUN_HOME + os.path.sep + "out"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, 'output.txt')
OUTPUT_FILE_ASYNC = os.path.join(OUTPUT_FOLDER, 'output_async.txt')
TEST_LOG = os.path.join(OUTPUT_FOLDER, 'testLog.txt')
VERBOSE_LOG = os.path.join(OUTPUT_FOLDER, 'verboseLog.txt')

# Default Simulator and Emulator settings
EMULATOR_NAME = "Emulator-Api19-Default"
EMULATOR_PORT = "5554"
EMULATOR_ID = "emulator-{0}".format(EMULATOR_PORT)
SIMULATOR_NAME = "iPhone7N"
SIMULATOR_TYPE = 'iPhone 7'
SIMULATOR_SDK = '10.0'

# Android Build Settings
ANDROID_KEYSTORE_PATH = os.environ.get("ANDROID_KEYSTORE_PATH")
ANDROID_KEYSTORE_PASS = os.environ.get("ANDROID_KEYSTORE_PASS")
ANDROID_KEYSTORE_ALIAS = os.environ.get("ANDROID_KEYSTORE_ALIAS")
ANDROID_KEYSTORE_ALIAS_PASS = os.environ.get("ANDROID_KEYSTORE_ALIAS_PASS")

# iOS Build Settings
DEVELOPMENT_TEAM = os.environ.get("DEVELOPMENT_TEAM")
