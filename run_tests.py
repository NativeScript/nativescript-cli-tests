# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# W0602 - Using global for %r but no assignment is done
# W0603 - Using the global statement
# pylint: disable=C0103, C0111, W0602, W0603
"""
Entry point of functional tests
"""


import os, platform
import core.cli


from helpers._os_lib import cleanup_folder, remove, run_aut, uninstall_app, cleanup_xcode_cache
from helpers._tns_lib import get_android_runtime, get_ios_runtime, \
    ANDROID_RUNTIME_SYMLINK_PATH, IOS_RUNTIME_SYMLINK_PATH, ANDROID_RUNTIME_PATH, IOS_RUNTIME_PATH
from helpers.device import stop_emulators
from helpers.simulator import stop_simulators

import tns_tests_runner


SMOKETESTRESULT = ""

def execute_tests():
    print "####RUNNING TESTS####"
    global SMOKETESTRESULT
    SMOKETESTRESULT = str(tns_tests_runner.run_tests())

def analyze_result_and_exit():
    global SMOKETESTRESULT
    if not "errors=0" in SMOKETESTRESULT or not "failures=0" in SMOKETESTRESULT:
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':

    # Run pylint
    run_aut("pylint tests", write_to_file="pylint_tests.log")
    run_aut("pylint helpers", write_to_file="pylint_helpers.log")
    run_aut("pylint run_tests.py", write_to_file="pylint_run_tests.log")
    run_aut("pylint tns_tests_runner.py", write_to_file="pylint_tns_tests_runner.log")

    # Clean NPM cache
    if 'Windows' in platform.platform():
        run_aut("npm cache clean", 600)
    else:
        run_aut("rm -rf ~/.npm/tns/*", 600)

    # Stop emulators and simulators
    stop_emulators()
    stop_simulators()

    if 'TEST_RUN' in os.environ and "FULL" in os.environ['TEST_RUN']:

        # Install ddb
        output = run_aut("ddb")
        if "Device Debug Bridge" not in output:
            run_aut("npm i -g ddb")

        # Uninstall test apps on real devices
        uninstall_app("TNSApp", platform="android", fail=False)
        uninstall_app("TNSAppNoPlatform", platform="android", fail=False)

        uninstall_app("TNSApp", platform="ios", fail=False)
        uninstall_app("TNSAppNoPlatform", platform="ios", fail=False)

        # Clean .gradle
        if 'Windows' in platform.platform():
            run_aut("rmdir /s /q {USERPROFILE}\\.gradle".format(**os.environ), 600)
        else:
            run_aut("rm -rf ~/.gradle", 600)

    # Clean old runtimes
    cleanup_folder(os.path.split(ANDROID_RUNTIME_SYMLINK_PATH)[0])
    cleanup_folder(os.path.split(IOS_RUNTIME_SYMLINK_PATH)[0])
    if os.path.isfile(ANDROID_RUNTIME_PATH):
        os.remove(ANDROID_RUNTIME_PATH)
    if os.path.isfile(IOS_RUNTIME_PATH):
        os.remove(IOS_RUNTIME_PATH)

    # cleanup files and folders created by the test execution
    remove('stderr.txt')
    remove('commands.txt')
    cleanup_folder('app')
    cleanup_folder('appTest')
    cleanup_folder('TNS App')
    cleanup_folder('TNS_App')
    cleanup_folder('TNS_TempApp')
    cleanup_folder('folder')
    cleanup_folder('template')
    cleanup_folder('tns_modules')
    cleanup_folder('tns_helloworld_app')
    cleanup_folder('node_modules')

    # uninstall/install CLI
    core.cli.uninstall()
    core.cli.install()

    # Get latest Android and iOS runtimes
    get_android_runtime()
    if 'Darwin' in platform.platform():
        get_ios_runtime()

    # Clone template-hello-world repo
    cleanup_folder('template-hello-world')
    OUTPUT = run_aut('git clone ' + \
                    'git@github.com:NativeScript/template-hello-world.git ' + \
                    'template-hello-world')
    assert not ("fatal" in OUTPUT), \
        "Failed to clone git@github.com:NativeScript/template-hello-world.git"

    # Clone template-hello-world-ts repo
    cleanup_folder('template-hello-world-ts')
    OUTPUT = run_aut('git clone ' + \
                    'git@github.com:NativeScript/template-hello-world-ts.git ' + \
                    'template-hello-world-ts')
    assert not ("fatal" in OUTPUT), \
        "Failed to clone git@github.com:NativeScript/template-hello-world-ts.git"

    # Clone QA-TestApps repo
    cleanup_folder('QA-TestApps')
    OUTPUT = run_aut(
        "git clone git@github.com:NativeScript/QA-TestApps.git QA-TestApps")
    assert not (
        "fatal" in OUTPUT), "Failed to clone git@github.com:NativeScript/QA-TestApps.git"

    # Clean Xcode cache and Derived data
    if 'Darwin' in platform.platform():
        cleanup_xcode_cache()

    # Execute tests
    execute_tests()

    # Stop running emulators
    if 'TEST_RUN' in os.environ and not "SMOKE" in os.environ['TEST_RUN']:
        stop_emulators()
        if 'Darwin' in platform.platform():
            stop_simulators()

    # Exit
    analyze_result_and_exit()
