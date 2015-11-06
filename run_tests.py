"""
Entry point of functional tests
"""
import platform
import os

from helpers._os_lib import cleanup_folder, remove, run_aut, uninstall_app
from helpers._tns_lib import uninstall_cli, install_cli, get_android_runtime, get_ios_runtime, \
    ANDROID_RUNTIME_SYMLINK_PATH, IOS_RUNTIME_SYMLINK_PATH, ANDROID_RUNTIME_PATH, IOS_RUNTIME_PATH
from helpers.device import stop_emulators, stop_simulators
import tns_tests_runner


SMOKETESTRESULT = ""

# C0111 - Missing docstring
# W0603 - Using the global statement
# pylint: disable=C0111, W0603
def execute_tests():
    print "####RUNNING TESTS####"
    global SMOKETESTRESULT
    SMOKETESTRESULT = str(tns_tests_runner.run_tests())

# C0111 - Missing docstring
# W0602 - Using global for %r but no assignment is done
# pylint: disable=C0111, W0602
def analyze_result_and_exit():
    global SMOKETESTRESULT
    if not "errors=0" in SMOKETESTRESULT or not "failures=0" in SMOKETESTRESULT:
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':

    # Clean NPM cache, Derived Data and compilation symbols
    if 'Windows' in platform.platform():
        run_aut("npm cache clean", 600)
    else:
        run_aut("rm -rf ~/.npm/tns/*", 600)
        run_aut("rm -rf ~/Library/Developer/Xcode/DerivedData/", 600)
        run_aut("sudo rm -rf /var/folders/*", 600)

    # Stop emulators and simulators
    stop_emulators()
    stop_simulators()

    # Uninstall test apps on real devices (if FULL RUN)
    if 'TESTRUN' in os.environ and "FULL" in os.environ['TESTRUN']:
        uninstall_app("TNSApp", platform="android", fail=False)
        uninstall_app("TNSApp", platform="ios", fail=False)

    # Cleanup old runtimes
    cleanup_folder(os.path.split(ANDROID_RUNTIME_SYMLINK_PATH)[0])
    cleanup_folder(os.path.split(IOS_RUNTIME_SYMLINK_PATH)[0])
    if os.path.isfile(ANDROID_RUNTIME_PATH):
        os.remove(ANDROID_RUNTIME_PATH)
    if os.path.isfile(IOS_RUNTIME_PATH):
        os.remove(IOS_RUNTIME_PATH)

    # Cleanup folders created by test execution
    remove('stderr.txt')
    cleanup_folder('app')
    cleanup_folder('appTest')
    cleanup_folder('TNS App')
    cleanup_folder('TNS_App')
    cleanup_folder('TNS_TempApp')
    cleanup_folder('folder')
    cleanup_folder('template')
    cleanup_folder('tns_modules')
    cleanup_folder('tns_helloworld_app')

    # Uninstall previous CLI and install latest
    uninstall_cli()
    install_cli()

    # Get latest Android and iOS runtimes
    get_android_runtime()
    if 'Darwin' in platform.platform():
        get_ios_runtime()

    # Clone hello-world template repo
    cleanup_folder('template-hello-world')
    OUTPUT = run_aut('git clone '
                    'git@github.com:NativeScript/template-hello-world.git '
                    'template-hello-world')
    assert not ("fatal" in OUTPUT), \
        'Failed to clone git@github.com:NativeScript/template-hello-world.git'

    # Clone QA-TestApps repo
    cleanup_folder('QA-TestApps')
    OUTPUT = run_aut(
        "git clone git@github.com:NativeScript/QA-TestApps.git QA-TestApps")
    assert not (
        "fatal" in OUTPUT), "Failed to clone git@github.com:NativeScript/QA-TestApps.git"

    # Execute tests
    execute_tests()

    # Stop running emulators
    if 'TESTRUN' in os.environ and not "SMOKE" in os.environ['TESTRUN']:
        stop_emulators()
        if 'Darwin' in platform.platform():
            stop_simulators()

    # Exit
    analyze_result_and_exit()
