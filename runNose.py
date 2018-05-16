import os
import shutil
import sys

import nose

from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.git.git import Git
from core.gradle.gradle import Gradle
from core.installer.cli import Cli
from core.npm.npm import Npm
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import OUTPUT_FOLDER, CURRENT_OS, OSType, \
    ANDROID_PATH, IOS_PATH, SUT_FOLDER, CLI_PATH, IOS_INSPECTOR_PATH, SIMULATOR_NAME, SIMULATOR_TYPE, SIMULATOR_SDK, \
    TEST_RUN_HOME
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.xcode.xcode import Xcode

reload(sys)

sys.setdefaultencoding('UTF8')


def disable_crash_report():
    if CURRENT_OS == OSType.OSX:
        run("defaults write com.apple.CrashReporter DialogType none")
        run("defaults write -g ApplePersistence -bool no")


def get_test_packages(platform=Platform.BOTH):
    """Copy {N} CLI form CLI_PATH to local folder"""
    shutil.copy2(CLI_PATH.strip(), SUT_FOLDER)
    shutil.copy2(ANDROID_PATH.strip(), SUT_FOLDER)
    if platform is Platform.BOTH or platform is Platform.IOS:
        shutil.copy2(IOS_PATH.strip(), SUT_FOLDER)
        shutil.copy2(IOS_INSPECTOR_PATH.strip(), SUT_FOLDER)


def get_repos():
    """
    Clone template-hello-world repositories
    """
    Git.clone_repo(repo_url='git@github.com:NativeScript/template-hello-world.git',
                   local_folder=os.path.join(SUT_FOLDER, 'template-hello-world'))
    Git.clone_repo(repo_url='git@github.com:NativeScript/template-hello-world-ts.git',
                   local_folder=os.path.join(SUT_FOLDER, 'template-hello-world-ts'))

    # `nativescript-angular` do not longer use release branch
    Git.clone_repo(repo_url='git@github.com:NativeScript/template-hello-world-ng.git',
                   local_folder=os.path.join(SUT_FOLDER, 'template-hello-world-ng'))

    Npm.pack(folder=os.path.join(SUT_FOLDER, 'template-hello-world'),
             output_file=os.path.join(SUT_FOLDER, 'tns-template-hello-world.tgz'))
    Npm.pack(folder=os.path.join(SUT_FOLDER, 'template-hello-world-ts'),
             output_file=os.path.join(SUT_FOLDER, 'tns-template-hello-world-ts.tgz'))
    Npm.pack(folder=os.path.join(SUT_FOLDER, 'template-hello-world-ng'),
             output_file=os.path.join(SUT_FOLDER, 'tns-template-hello-world-ng.tgz'))


if __name__ == '__main__':

    # Cleanup files and folders created by the test execution
    Folder.cleanup(OUTPUT_FOLDER)
    Folder.create(OUTPUT_FOLDER)
    Folder.cleanup(SUT_FOLDER)
    Folder.cleanup("node_modules")
    Npm.cache_clean()
    Gradle.kill()
    Gradle.cache_clean()
    get_repos()
    Emulator.stop()  # Stop running emulators

    # Copy test packages and cleanup
    if CURRENT_OS == OSType.OSX:
        Simulator.stop()
        disable_crash_report()
        get_test_packages(platform=Platform.BOTH)
        Simulator.reset()

        if "8." in Xcode.get_version():
            SIMULATOR_SDK = '10.0'

        Simulator.create(SIMULATOR_NAME, SIMULATOR_TYPE, SIMULATOR_SDK)
        Xcode.cleanup_cache()  # Clean Xcode cache folders
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.IOS)
    else:
        get_test_packages(platform=Platform.ANDROID)

    # Install CLI
    Cli.install()
    Tns.disable_reporting()

    # Add local CLI to PATH
    if CURRENT_OS != OSType.WINDOWS:
        base_path = os.path.join(TEST_RUN_HOME, 'node_modules', 'nativescript', 'bin')
        where_command = 'which tns'
    else:
        base_path = os.path.join(TEST_RUN_HOME, 'node_modules', '.bin')
        where_command = 'where tns'
    path = base_path + os.pathsep + os.environ['PATH']
    os.environ['PATH'] = path
    assert 'not found' not in run(command='tns --version'), 'Tns global installation not found!'
    assert base_path in run(command=where_command), 'Global installation is not the local one!'

    # Run Tests
    arguments = ['nosetests', '-v', '-s', '--nologcapture', '--with-doctest', '--with-xunit', '--with-flaky']
    for i in sys.argv:
        arguments.append(str(i))
    nose.run(argv=arguments)

    # Cleanup and reset after test run is complete
    if CURRENT_OS == OSType.OSX:
        Simulator.reset()
        Gradle.kill()
        Gradle.cache_clean()
