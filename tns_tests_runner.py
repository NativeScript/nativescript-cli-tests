"""
Define test suites
"""
import os
import platform
import unittest

from helpers import HTMLTestRunner
from helpers._tns_lib import get_cli_version
from tests.autocomplete import Autocomplete
from tests.build_linux import BuildAndroid
from tests.build_osx import BuildiOS
from tests.create import Create
from tests.debug_linux import DebugAndroid
from tests.debug_osx import DebugiOS
from tests.deploy_linux import DeployAndroid
from tests.deploy_osx import DeployiOS
from tests.device_linux import DeviceAndroid
from tests.device_osx import DeviceiOS
from tests.doctor import Doctor
from tests.emulate_linux import EmulateAndroid
from tests.emulate_osx import EmulateiOS
from tests.initinstall import InitAndInstall
from tests.library_linux import LibraryAndroid
from tests.library_osx import LibraryiOS
from tests.livesync_android import LiveSyncAndroid
from tests.livesync_emulator import LiveSyncEmulator
from tests.livesync_ios import LiveSynciOS
from tests.livesync_simulator import LiveSyncSimulator
from tests.logtrace import LogTrace
from tests.output_stderr import Output_STRERR
from tests.platform_linux import PlatformAndroid
from tests.platform_osx import PlatformiOS
from tests.plugins_linux import PluginsAndroid
from tests.plugins_osx import PluginsiOS
from tests.plugins_osx_libs import PluginsiOSLibs
from tests.plugins_osx_pods import PluginsiOSPods
from tests.plugins_osx_sandbox_pods import PluginsiOSSandboxPods
from tests.plugins_osx_xcconfig import PluginsiOSXcconfig
from tests.prepare_linux import PrepareAndroid
from tests.prepare_osx import PrepareiOS
from tests.run_osx import RuniOS
from tests.transpilation_typescript import TranspilationTypeScript
from tests.usage import UsageAndErrorTracking
from tests.version import Version


# C0111 - Missing docstring
# R0915 - Too many statements
# W0212 - Access to a protected member
# W0640 - Cell variable test defined in loop
# pylint: disable=C0111, R0915, W0212, W0640

def run_tests():

    print "Platform : ", platform.platform()

    # Android Requirements:
    # - Valid pair of keystore and password
    #
    # iOS Requirements:
    # - Valid pair of certificate and provisioning profile on your OS X system
    #
    # Following environment variables should be set:
    # - CLI_PATH - Path to CLI package under test (package file should be named nativescript.tgz)
    #
    # - ANDROID_PATH - Path to Android runtime package (should be named tns-android.tgz)
    # - ANDROID_KEYSTORE_PATH - Path to the keystore file
    # - ANDROID_KEYSTORE_PASS - Password for the keystore file
    # - ANDROID_KEYSTORE_ALIAS
    # - ANDROID_KEYSTORE_ALIAS_PASS
    #
    # - IOS_PATH - Path to iOS runtime package (should be named tns-ios.tgz)
    #
    # - ACTIVE_UI - YES or NO
    #
    # - TEST_RUN - types:
    # SMOKE
    # - Runs tests with High priority.
    # DEFAULT
    # - All suites without dependencies on real devices  (all priorities)
    # - Following AVDs should be available
    #    Api19 - Android emulator with API19
    # FULL
    # - Runs all tests
    # - At least one real Android device must be attached to Linux hosts
    # - At least one real iOS device must be attached to OSX hosts
    #
    # LIVESYNC
    # - Runs all LiveSync tests
    #
    # Test name convention:
    # 001 - 199 - High priority
    # 200 - 299 - Medium priority
    # 300 - 399 - Low priority
    # 400 - 499 - Negative tests

    suite = unittest.TestLoader().loadTestsFromTestCase(Version)
    # Temporary ignore Help tests because of expected breaking changes
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Help))

    if ('TEST_RUN' in os.environ) and ("LIVESYNC" in os.environ['TEST_RUN']):
        if 'Darwin' in platform.platform():
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncSimulator))
            # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSynciOS))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncEmulator))
            # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncAndroid))
        if 'Windows' in platform.platform():
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncEmulator))
    else:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LogTrace))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Autocomplete))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(UsageAndErrorTracking))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Output_STRERR))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Doctor))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Create))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PlatformAndroid))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PrepareAndroid))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(BuildAndroid))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsAndroid))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(InitAndInstall))
        if 'Darwin' in platform.platform():
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PlatformiOS))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PrepareiOS))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(BuildiOS))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOS))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOSSandboxPods))

        if ('TEST_RUN' in os.environ) and (not "SMOKE" in os.environ['TEST_RUN']):
            if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']):
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(EmulateAndroid))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LibraryAndroid))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TranspilationTypeScript))
            if 'Darwin' in platform.platform():
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(EmulateiOS))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LibraryiOS))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOSPods))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOSLibs))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOSXcconfig))

        if ('TEST_RUN' in os.environ) and ("FULL" in os.environ['TEST_RUN']):
            suite.addTests(
                unittest.TestLoader().loadTestsFromTestCase(DeployAndroid))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(RuniOS))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DeviceAndroid))
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DebugAndroid))
            if 'Darwin' in platform.platform():
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DeployiOS))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(RuniOS))
#                 suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncSimulator))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSynciOS))
#                 suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncEmulator))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncAndroid))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DeviceiOS))
                suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DebugiOS))

    # Smoke test runs only high priority tests
    if ('TEST_RUN' in os.environ) and ("SMOKE" in os.environ['TEST_RUN']):
        for test in suite:
            if test._testMethodName.find('test_4') >= 0:
                setattr(test, test._testMethodName, lambda: test.skipTest(
                    'Skip negative tests in SMOKE TEST run.'))
            if test._testMethodName.find('test_3') >= 0:
                setattr(test, test._testMethodName, lambda: test.skipTest(
                    'Skip low priority tests in SMOKE TEST run.'))
            if test._testMethodName.find('test_2') >= 0:
                setattr(test, test._testMethodName, lambda: test.skipTest(
                    'Skip medium priority tests in SMOKE TEST run.'))

    with open("Report.html", "w") as report:
        descr = "Platform : {0};  nativescript-cli build version : {1}" \
                .format(platform.platform(), get_cli_version())
        runner = HTMLTestRunner.HTMLTestRunner(
            report, title='TNS_CLI_tests', description=descr)
        result = runner.run(suite)
    return result

if __name__ == '__main__':
    run_tests()
