import os
import shutil
import sys
import tarfile

import nose

from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.installer.cli import Cli
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import OUTPUT_FOLDER, CURRENT_OS, OSType, \
    COMMAND_TIMEOUT, ANDROID_PATH, IOS_PATH, SUT_ROOT_FOLDER, TEST_RUN, CLI_PATH, ANDROID_RUNTIME_PATH, \
    IOS_RUNTIME_PATH, TNS_MODULES_PATH, TNS_MODULES_WIDGETS_PATH
from core.tns.tns import Tns
from core.xcode.xcode import Xcode

reload(sys)

sys.setdefaultencoding('UTF8')


def clone_git_repo(repo_url, local_folder):
    branch = 'master'
    if 'release' in TNS_MODULES_PATH.lower():
        branch = 'release'
    output = run('git clone -b ' + branch + ' ' + repo_url + ' ' + local_folder)
    assert not ("fatal" in output), \
        "Failed to clone {0}".format(repo_url)


def clean_npm():
    if CURRENT_OS == OSType.WINDOWS:
        run("npm cache clean", COMMAND_TIMEOUT)
    else:
        run("npm cache clean", COMMAND_TIMEOUT)
        run("rm -rf ~/.npm/tns*", COMMAND_TIMEOUT)

def clean_gradle():
    if CURRENT_OS == OSType.WINDOWS:
        run("rmdir /s /q {USERPROFILE}\\.gradle".format(**os.environ), COMMAND_TIMEOUT)
    else:
        run("rm -rf ~/.gradle", 600)


def get_cli():
    """Copy {N} CLI form CLI_PATH to local folder"""
    location = os.path.join(CLI_PATH, "nativescript.tgz")
    shutil.copy2(location.strip(), os.path.join(os.getcwd(), SUT_ROOT_FOLDER, "nativescript.tgz"))


def extract_archive(file_name, folder):
    """Extract archive"""
    if file_name.endswith(".tgz"):
        tar = tarfile.open(file_name)
        tar.extractall(path=os.path.join(os.getcwd(), folder))
        tar.close()
        print "{0} extracted in {1}".format(file_name, folder)
    else:
        print "Failed to extract {0}".format(file_name)


def get_tns_core_modules():
    """Copy tns-core-modules.tgz and tns-platform-declarations.tgz to local folder"""
    location = os.path.join(TNS_MODULES_PATH, "tns-core-modules.tgz")
    shutil.copy2(location.strip(), os.path.join(os.getcwd(), SUT_ROOT_FOLDER, "tns-core-modules.tgz"))
    location = os.path.join(TNS_MODULES_PATH, "tns-platform-declarations.tgz")
    shutil.copy2(location.strip(), os.path.join(os.getcwd(), SUT_ROOT_FOLDER, "tns-platform-declarations.tgz"))


def get_tns_core_modules_widgets():
    """Copy tns-core-modules-widgets.tgz to local folder"""
    location = os.path.join(TNS_MODULES_WIDGETS_PATH, "tns-core-modules-widgets.tgz")
    shutil.copy2(location.strip(), os.path.join(os.getcwd(), SUT_ROOT_FOLDER, "tns-core-modules-widgets.tgz"))


def get_android_runtime():
    """Copy android runtime form ANDROID_PATH to local folder"""
    location = os.path.join(ANDROID_PATH, "tns-android.tgz")
    shutil.copy2(location.strip(), os.path.join(os.getcwd(), SUT_ROOT_FOLDER, "tns-android.tgz"))
    if File.exists(os.path.join(os.getcwd(), ANDROID_RUNTIME_PATH)):
        extract_archive(ANDROID_RUNTIME_PATH, os.path.splitext(ANDROID_RUNTIME_PATH)[0])


def get_ios_runtime():
    """Copy android runtime form IOS_PATH to local folder"""
    location = os.path.join(IOS_PATH, "tns-ios.tgz")
    shutil.copy2(location.strip(), os.path.join(os.getcwd(), SUT_ROOT_FOLDER, "tns-ios.tgz"))
    if File.exists(os.path.join(os.getcwd(), IOS_RUNTIME_PATH)):
        extract_archive(IOS_RUNTIME_PATH, os.path.splitext(IOS_RUNTIME_PATH)[0])


def get_repos():
    # Clone template-hello-world repos (both js and ts)
    clone_git_repo("git@github.com:NativeScript/template-hello-world.git", SUT_ROOT_FOLDER + "/template-hello-world")
    clone_git_repo("git@github.com:NativeScript/template-hello-world-ts.git",
                   SUT_ROOT_FOLDER + "/template-hello-world-ts")

    # Clone QA-TestApps repo
    clone_git_repo("git@github.com:NativeScript/QA-TestApps.git", SUT_ROOT_FOLDER + "/QA-TestApps")
    # TODO: QA-TestApps is privite, we should make it public or move all test data to data folder#


def get_package():
    location = os.path.join(ANDROID_PATH, "tns-android.tgz")
    shutil.copy2(location.strip(), os.path.join(os.getcwd(), SUT_ROOT_FOLDER, "tns-core-modules-widgets.tgz"))


if __name__ == '__main__':

    # Cleanup files and folders created by the test execution
    Folder.cleanup(OUTPUT_FOLDER)
    Folder.create(OUTPUT_FOLDER)
    Folder.cleanup(SUT_ROOT_FOLDER)
    Folder.cleanup("node_modules")
    clean_npm()  # Clean NPM cache
    clean_gradle()  # Clean Gradle
    get_repos()  # Clone test repos
    Emulator.stop_emulators()  # Stop running emulators

    # Copy test packages and cleanup
    get_cli()  # Get {N} CLI
    get_tns_core_modules()  # Get core modules
    get_tns_core_modules_widgets()  # Get widgets (dependency of core modules)
    get_android_runtime()  # Get Android Runtime
    if CURRENT_OS == OSType.OSX:
        Simulator.stop_simulators()  # Stop running simulators
        Xcode.cleanup_cache()  # Clean Xcode cache folders
        get_ios_runtime()  # Get iOS Runtime
    if TEST_RUN == "RUN":
        Device.uninstall_app("org.nativescript.", platform="android", fail=False)
        if CURRENT_OS == OSType.OSX:
            Device.uninstall_app("org.nativescript.", platform="ios", fail=False)

    # Install CLI
    Cli.install()
    Tns.disable_reporting()

    arguments = ['nosetests', '-v', '-s', '--nologcapture', '--with-doctest', '--with-xunit']
    for i in sys.argv:
        arguments.append(str(i))
    nose.run(argv=arguments)
