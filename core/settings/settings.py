"""
Settings
"""
import os
import platform

from core.osutils.os_type import OSType


def resolve_package(package_env, default_value):
    package = default_value
    package_env_value = os.getenv(package_env)
    package_env_value_with_dash = os.getenv(package_env.replace("-", "_"))

    if package_env_value is None and package_env_value_with_dash is None:
        print "{0} not set.".format(package_env)
    elif package_env_value is not None:
        if '.tgz' in package_env_value:
            package = package_env_value
            print "{0} tgz package found.".format(package)
        else:
            package = "{0}@{1}".format(package_env, package_env_value)
            print "{0} npm package found.".format(package)
    elif package_env_value_with_dash is not None:
        if '.tgz' in package_env_value_with_dash:
            package = package_env_value_with_dash
            print "{0} tgz package found.".format(package_env_value_with_dash)
        else:
            package = "{0}@{1}".format(package_env, package_env_value_with_dash)
            print "{0} npm package found.".format(package)

    return package


def resolve_path(package_env, default_value):
    package = default_value
    package_env_value = os.environ.get(package_env)
    if package_env_value is None:
        print "{0} not set.".format(package_env)
    elif '.tgz' in package_env_value:
        package = package_env_value
    else:
        # At the moment if we pass nativescript=rc we will still get default path.
        # TODO: Make it more flexible.
        package = default_value
    return package


# Timeout settings (in seconds)
COMMAND_TIMEOUT = 600

# Set current OS
CURRENT_OS = OSType.LINUX
if "Windows" in platform.platform():
    CURRENT_OS = OSType.WINDOWS
if "Darwin" in platform.platform():
    CURRENT_OS = OSType.OSX

# Set test run root folder
TEST_RUN_HOME = os.getcwd()

# Test packages location from env. variables
BASE_PACKAGE_PATH = os.environ.get("BASE_PACKAGE", "Missing")
if "Missing" in BASE_PACKAGE_PATH:
    BASE_PACKAGE_PATH = os.environ.get("BASE_PACKAGE_PATH", "/tns-dist")

BRANCH = os.environ.get("CLI_PACKAGES_BRANCH", "missing").lower()
if "missing" in BRANCH :
    BRANCH = os.environ.get("BRANCH", "master").lower()

if "release" in BRANCH:
    SHARE_BRANCH = "Release"
    TAG = "rc"
else:
    SHARE_BRANCH = "Stable"
    TAG = "next"

# Set source location of separate package based on base path


CLI_PATH = os.environ.get("CLI_PATH", os.path.join(BASE_PACKAGE_PATH, "CLI", SHARE_BRANCH, "nativescript.tgz"))
ANDROID_PATH = os.environ.get("ANDROID_PATH",
                              os.path.join(BASE_PACKAGE_PATH, "tns-android", SHARE_BRANCH, "tns-android.tgz"))
IOS_PATH = os.environ.get("IOS_PATH", os.path.join(BASE_PACKAGE_PATH, "tns-ios", SHARE_BRANCH, "tns-ios.tgz"))
TNS_MODULES_PATH = os.environ.get("TNS_MODULES_PATH",
                                  os.path.join(BASE_PACKAGE_PATH, "tns-modules", SHARE_BRANCH, "tns-core-modules.tgz"))
IOS_INSPECTOR_PATH = os.environ.get("IOS_INSPECTOR_PATH",
                                    os.path.join(BASE_PACKAGE_PATH, "tns-ios-inspector", SHARE_BRANCH,
                                                 "tns-ios-inspector.tgz"))

# Root folder for local packages
SUT_FOLDER = os.path.join(TEST_RUN_HOME, "sut")

# Set local location of test packages
TNS_PATH = os.path.join("node_modules", ".bin", "tns")
UPDATE_WEBPACK_PATH = os.path.join("node_modules", ".bin", "update-ns-webpack")
ANDROID_PACKAGE = os.path.join(SUT_FOLDER, "tns-android.tgz")
IOS_PACKAGE = os.path.join(SUT_FOLDER, "tns-ios.tgz")
IOS_INSPECTOR_PACKAGE = os.path.join(SUT_FOLDER, "tns-ios-inspector.tgz")

# Respect path variables
CLI_PATH = resolve_path("nativescript", CLI_PATH)
ANDROID_PATH = resolve_path("android", ANDROID_PATH)
IOS_PATH = resolve_path("ios", IOS_PATH)
IOS_INSPECTOR_PATH = resolve_path("ios-inspector", IOS_INSPECTOR_PATH)
WEBPACK_PACKAGE = resolve_package("nativescript-dev-webpack", "nativescript-dev-webpack@next")
SASS_PACKAGE = resolve_package("nativescript-dev-sass", "nativescript-dev-sass@next")
TYPESCRIPT_PACKAGE = resolve_package("nativescript-dev-typescript", "nativescript-dev-typescript@next")
ANGULAR_PACKAGE = resolve_package("nativescript-angular", "nativescript-angular@next")
MODULES_PACKAGE = resolve_package("tns-core-modules", "tns-core-modules@{0}".format(TAG))

# Output settings
OUTPUT_FOLDER = TEST_RUN_HOME + os.path.sep + "out"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, 'output.txt')
OUTPUT_FILE_ASYNC = os.path.join(OUTPUT_FOLDER, 'output_async.txt')
TEST_LOG = os.path.join(OUTPUT_FOLDER, 'testLog.txt')
VERBOSE_LOG = os.path.join(OUTPUT_FOLDER, 'verboseLog.txt')

# Default Simulator and Emulator settings
EMULATOR_NAME = "Emulator-Api23-Default"
EMULATOR_PORT = "5554"
EMULATOR_ID = "emulator-{0}".format(EMULATOR_PORT)
SIMULATOR_NAME = "iPhone7N"
SIMULATOR_TYPE = 'iPhone 7'
SIMULATOR_SDK = '11.0'

# Android Build Settings
ANDROID_KEYSTORE_PATH = os.environ.get("ANDROID_KEYSTORE_PATH")
ANDROID_KEYSTORE_PASS = os.environ.get("ANDROID_KEYSTORE_PASS")
ANDROID_KEYSTORE_ALIAS = os.environ.get("ANDROID_KEYSTORE_ALIAS")
ANDROID_KEYSTORE_ALIAS_PASS = os.environ.get("ANDROID_KEYSTORE_ALIAS_PASS")

# iOS Build Settings
DEVELOPMENT_TEAM = os.environ.get("DEVELOPMENT_TEAM")
PROVISIONING = os.environ.get("PROVISIONING")
DISTRIBUTION_PROVISIONING = os.environ.get("DISTRIBUTION_PROVISIONING")
