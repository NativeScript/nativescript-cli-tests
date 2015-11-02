"""
Entry point of functional tests
"""
import platform, os

from helpers._os_lib import CleanupFolder, remove, runAUT, uninstall_app
from helpers._tns_lib import UninstallCLI, InstallCLI, GetAndroidRuntime, GetiOSRuntime, \
    androidRuntimeSymlinkPath, iosRuntimeSymlinkPath, androidRuntimePath, iosRuntimePath
from helpers.device import StopEmulators, StopSimulators
import tns_tests_runner


SMOKETESTRESULT = ""

def ExecuteTests():
    print "####RUNNING TESTS####"
    global SMOKETESTRESULT
    SMOKETESTRESULT = str(tns_tests_runner.RunTests())

def AnalyzeResultAndExit():
    global SMOKETESTRESULT
    if not "errors=0" in SMOKETESTRESULT or not "failures=0" in SMOKETESTRESULT:
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':
    # Clean NPM cache, Derived Data and compilation symbols
    if 'Windows' in platform.platform():
        runAUT("npm cache clean", 600)
    else:
        runAUT("rm --rf ~/.npm/tns/*", 600)
        runAUT("rm --rf ~/Library/Developer/Xcode/DerivedData/", 600)
        runAUT("sudo rm --rf /var/folders/*", 600)
    # Uninstall test apps
    uninstall_app("TNSApp", platform="android", fail=False)
    uninstall_app("TNSApp", platform="ios", fail=False)
    # Cleanup old runtimes
    CleanupFolder(os.path.split(androidRuntimeSymlinkPath)[0])
    CleanupFolder(os.path.split(iosRuntimeSymlinkPath)[0])
    if os.path.isfile(androidRuntimePath):
        os.remove(androidRuntimePath)
    if os.path.isfile(iosRuntimePath):
        os.remove(iosRuntimePath)
    # Cleanup folders created by test execution
    remove('stderr.txt')
    CleanupFolder('app')
    CleanupFolder('appTest')
    CleanupFolder('TNS App')
    CleanupFolder('TNS_App')
    CleanupFolder('TNS_TempApp')
    CleanupFolder('folder')
    CleanupFolder('template')
    CleanupFolder('tns_modules')
    CleanupFolder('tns_helloworld_app')
    # Uninstall previous CLI and install latest
    UninstallCLI()
    InstallCLI()
    # Get latest Android and iOS runtimes
    GetAndroidRuntime()
    if 'Darwin' in platform.platform():
        GetiOSRuntime()
    # Clone hello-world template repo
    CleanupFolder('template-hello-world')
    OUTPUT = runAUT('git clone '
                    'git@github.com:NativeScript/template-hello-world.git '
                    'template-hello-world')
    assert not ("fatal" in OUTPUT), \
        'Failed to clone git@github.com:NativeScript/template-hello-world.git'
    # Clone QA-TestApps repo
    CleanupFolder('QA-TestApps')
    OUTPUT = runAUT("git clone git@github.com:NativeScript/QA-TestApps.git QA-TestApps")
    assert not ("fatal" in OUTPUT), "Failed to clone git@github.com:NativeScript/QA-TestApps.git"
    # Execute tests
    ExecuteTests()
    # Stop running emulators
    if 'TESTRUN' in os.environ and not "SMOKE" in os.environ['TESTRUN']:
        StopEmulators()
        if 'Darwin' in platform.platform():
            StopSimulators()
    # Exit
    AnalyzeResultAndExit()