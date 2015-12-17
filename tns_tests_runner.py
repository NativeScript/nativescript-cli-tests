# C0111 - Missing docstring
# W0212 - Access to a protected member
# W0640 - Cell variable test defined in loop
# pylint: disable=C0111, W0212, W0640


import os, platform, unittest

from core.tns import Tns
from helpers import HTMLTestRunner

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
from tests.livesync_emulator_full import LivesyncEmulatorFull
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

from tests.error import Error
from tests.unittests import UnitTests
from tests.usage import Usage
from tests.version import Version


def run_tests():

    print "Platform : " + platform.platform()
    suite = unittest.TestLoader().loadTestsFromTestCase(Version)

    def suite_smoke():


        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Usage))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Error))


        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LogTrace))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Autocomplete))
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

    def suite_default():


        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(UnitTests))


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

    def suite_run():
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

    def suite_livesync():
        if 'Darwin' in platform.platform():
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncSimulator))
            # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSynciOS))
#             suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncEmulator))
            # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncAndroid))
        if 'Windows' in platform.platform():
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LivesyncEmulatorFull))
            # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LiveSyncEmulator))

    # TODO: Uncomment Help Tests
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Help))


    if 'SMOKE' in os.environ['TEST_RUN']:
        suite_smoke()
    elif 'DEFAULT' in os.environ['TEST_RUN']:
        suite_smoke()
        suite_default()
    elif 'RUN' in os.environ['TEST_RUN']:
        suite_run()
    elif 'LIVESYNC' in os.environ['TEST_RUN']:
        suite_livesync()
    elif 'FULL' in os.environ['TEST_RUN']:
        suite_smoke()
        suite_default()
        suite_run()
        suite_livesync()

    # Smoke suite runs only high priority tests
    if 'SMOKE' in os.environ['TEST_RUN']:
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

    with open("Report.html", "w") as report:
        descr = "Platform : {0}\n \
                {N} CLI build version : {1}\n \
                Test Suite : {2}".format(
                    platform.platform(),
                    Tns.version(),
                    os.environ['TEST_RUN'])
        runner = HTMLTestRunner.HTMLTestRunner(report, title='TNS_CLI_tests', description=descr)
        result = runner.run(suite)
    return result

if __name__ == '__main__':
    run_tests()
