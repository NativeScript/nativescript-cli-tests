import os
import platform
import unittest

from core.runner import HTMLTestRunner
from core.settings.settings import CURRENT_OS, OSType
from core.tns.tns import Tns
from tests.build.build_android import BuildAndroid
from tests.build.build_ios import BuildiOS
from tests.build.create import Create
from tests.build.initinstall import InitAndInstall
from tests.build.platform_android import PlatformAndroid
from tests.build.platform_ios import PlatformiOS
from tests.build.prepare_android import PrepareAndroid
from tests.build.prepare_ios import PrepareiOS
from tests.debug.debug_android import DebugAndroid
from tests.debug.debug_ios import DebugiOS
from tests.emulate.emulate_android import EmulateAndroid
from tests.emulate.emulate_ios import EmulateiOS
from tests.livesync.livesync_android import LiveSyncAndroid
from tests.livesync.livesync_emulator import LiveSyncEmulator
from tests.livesync.livesync_emulator_watch import LiveSyncEmulatorWatch
from tests.livesync.livesync_ios import LiveSynciOS
from tests.livesync.livesync_simulator import LiveSyncSimulator
from tests.other.autocomplete import Autocomplete
from tests.other.doctor import Doctor
from tests.other.error_reporting import ErrorReporting
from tests.other.logtrace import LogTrace
from tests.other.output_stderr import Output_STRERR
from tests.other.usage_reporting import Usage
from tests.other.version import Version
from tests.plugin.plugins_android import PluginsAndroid
from tests.plugin.plugins_ios import PluginsiOS
from tests.plugin.plugins_ios_libs import PluginsiOSLibs
from tests.plugin.plugins_ios_pods import PluginsiOSPods
from tests.plugin.plugins_ios_sandbox_pods import PluginsiOSSandboxPods
from tests.plugin.plugins_ios_xcconfig import PluginsiOSXcconfig
from tests.run.deploy_android import DeployAndroid
from tests.run.deploy_ios import DeployiOS
from tests.run.device_android import DeviceAndroid
from tests.run.device_ios import DeviceiOS
from tests.run.run_android import RunAndroid
from tests.run.run_ios import RuniOS
from tests.transpilers.typescript import TypeScript
from tests.unittests.unittests import UnitTests
from tests.unittests.unittests_emulator import UnitTestsEmulator
from tests.unittests.unittests_simulator import UnitTestsSimulator


def suite_smoke():
    suite = suite_build()
    # Smoke suite runs only high priority tests from build suite
    for test in suite:
        if test._testMethodName.find('test_4') >= 0:
            setattr(test, test._testMethodName, lambda: test.skipTest(
                    'Skip negative tests in SMOKE suite run.'))
        if test._testMethodName.find('test_3') >= 0:
            setattr(test, test._testMethodName, lambda: test.skipTest(
                    'Skip low priority tests in SMOKE suite run.'))
        if test._testMethodName.find('test_2') >= 0:
            setattr(test, test._testMethodName, lambda: test.skipTest(
                    'Skip medium priority tests in SMOKE suite run.'))
    return suite


def suite_build():
    suite = unittest.TestLoader().loadTestsFromTestCase(Version)
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Help))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Usage))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ErrorReporting))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LogTrace))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Autocomplete))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Output_STRERR))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Doctor))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Create))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PlatformAndroid))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PrepareAndroid))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(BuildAndroid))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(InitAndInstall))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TypeScript))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(UnitTests))
    if CURRENT_OS == OSType.OSX:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PlatformiOS))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PrepareiOS))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(BuildiOS))
    return suite


def suite_plugins():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsAndroid))
    if CURRENT_OS == OSType.OSX:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOS))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOSSandboxPods))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOSPods))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOSLibs))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginsiOSXcconfig))
    return suite


def suite_emulate():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(EmulateAndroid))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(UnitTestsEmulator))
    if CURRENT_OS == OSType.OSX:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(EmulateiOS))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(UnitTestsSimulator))
    return suite


def suite_run():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DeployAndroid))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DeviceAndroid))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(RunAndroid))
    if CURRENT_OS == OSType.OSX:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DeployiOS))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DeviceiOS))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(RuniOS))
    return suite


def suite_livesync():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncEmulator))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncEmulatorWatch))
    if CURRENT_OS == OSType.OSX:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncSimulator))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSynciOS))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncAndroid))
    return suite


def suite_debug():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DebugAndroid))
    if CURRENT_OS == OSType.OSX:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DebugiOS))
    return suite


def run_tests():
    print "Platform : " + platform.platform()

    suite = unittest.TestSuite()
    if 'SMOKE' in os.environ['TEST_RUN']:
        suite = suite_smoke()
    elif 'BUILD' in os.environ['TEST_RUN']:
        suite = suite_build()
    elif 'PLUGINS' in os.environ['TEST_RUN']:
        suite = suite_plugins()
    elif 'EMULATE' in os.environ['TEST_RUN']:
        suite = suite_emulate()
    elif 'RUN' in os.environ['TEST_RUN']:
        suite = suite_run()
    elif 'LIVESYNC' in os.environ['TEST_RUN']:
        suite = suite_livesync()
    elif 'DEBUG' in os.environ['TEST_RUN']:
        suite = suite_debug()

    with open("Report.html", "w") as report:
        descr = "Platform : {0}; NativeScript CLI build version : {1}; Test Suite : {2}".format(
                platform.platform(), Tns.version(), os.environ['TEST_RUN'])
        runner = HTMLTestRunner.HTMLTestRunner(report, title='TNS_CLI_tests', description=descr)
        result = runner.run(suite)
    return result


if __name__ == '__main__':
    run_tests()
