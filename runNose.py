import os
import shutil
import sys
import tarfile

import nose

from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.git.GitHub import GitHub
from core.installer.cli import Cli
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import OUTPUT_FOLDER, CURRENT_OS, OSType, \
    COMMAND_TIMEOUT, ANDROID_PATH, IOS_PATH, SUT_ROOT_FOLDER, CLI_PATH, ANDROID_RUNTIME_PATH, \
    IOS_RUNTIME_PATH, TNS_MODULES_PATH, TNS_MODULES_WIDGETS_PATH, IOS_INSPECTOR_PATH, TNS_PLATFORM_DECLARATIONS_PATH, \
    BRANCH
from core.tns.tns import Tns
from core.tns.tns_installed_platforms import Platforms
from core.xcode.xcode import Xcode

reload(sys)

sys.setdefaultencoding('UTF8')


def __extract_archive(file_name, folder):
    """Extract archive
    :param file_name: Archive file name.
    :param folder: Target folder.
    """
    if file_name.endswith(".tgz"):
        tar = tarfile.open(file_name)
        tar.extractall(path=os.path.join(os.getcwd(), folder))
        tar.close()
        print "{0} extracted in {1}".format(file_name, folder)
    else:
        print "Failed to extract {0}".format(file_name)


def clean_npm():
    """Clean npm cache"""
    if CURRENT_OS == OSType.WINDOWS:
        run("npm cache clean", COMMAND_TIMEOUT)
    else:
        run("npm cache clean", COMMAND_TIMEOUT)
        run("rm -rf ~/.npm/tns*", COMMAND_TIMEOUT)


def clean_gradle():
    """Clean gradle cache"""
    if CURRENT_OS == OSType.WINDOWS:
        run("rmdir /s /q {USERPROFILE}\\.gradle".format(**os.environ), COMMAND_TIMEOUT)
    else:
        run("rm -rf ~/.gradle", 600)


def get_test_packages(platform=Platforms.BOTH):
    """Copy {N} CLI form CLI_PATH to local folder"""
    shutil.copy2(CLI_PATH.strip(), SUT_ROOT_FOLDER)
    shutil.copy2(TNS_MODULES_PATH.strip(), SUT_ROOT_FOLDER)
    shutil.copy2(TNS_MODULES_WIDGETS_PATH.strip(), SUT_ROOT_FOLDER)
    shutil.copy2(ANDROID_PATH.strip(), SUT_ROOT_FOLDER)
    shutil.copy2(TNS_PLATFORM_DECLARATIONS_PATH.strip(), SUT_ROOT_FOLDER)

    if File.exists(os.path.join(os.getcwd(), ANDROID_RUNTIME_PATH)):
        __extract_archive(ANDROID_RUNTIME_PATH, os.path.splitext(ANDROID_RUNTIME_PATH)[0])

    if platform is Platforms.BOTH or platform is Platforms.IOS:
        shutil.copy2(IOS_PATH.strip(), SUT_ROOT_FOLDER)
        shutil.copy2(IOS_INSPECTOR_PATH.strip(), SUT_ROOT_FOLDER)
        if File.exists(os.path.join(os.getcwd(), IOS_RUNTIME_PATH)):
            __extract_archive(IOS_RUNTIME_PATH, os.path.splitext(IOS_RUNTIME_PATH)[0])


def get_repos():
    # Clone template-hello-world repos (both js and ts)
    GitHub.clone_repo(repo_url="git@github.com:NativeScript/template-hello-world.git",
                      local_folder=SUT_ROOT_FOLDER + "/template-hello-world", branch=BRANCH)
    GitHub.clone_repo(repo_url="git@github.com:NativeScript/template-hello-world-ts.git",
                      local_folder=SUT_ROOT_FOLDER + "/template-hello-world-ts", branch=BRANCH)

    # Clone QA-TestApps repo
    # TODO: QA-TestApps is privite, we should make it public or move all test data to data folder.
    GitHub.clone_repo(repo_url="git@github.com:NativeScript/QA-TestApps.git",
                      local_folder=SUT_ROOT_FOLDER + "/QA-TestApps", branch=BRANCH)


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
    if CURRENT_OS == OSType.OSX:
        get_test_packages(platform=Platforms.BOTH)
        Simulator.stop_simulators()  # Stop running simulators
        Xcode.cleanup_cache()  # Clean Xcode cache folders
    else:
        get_test_packages(platform=Platforms.ANDROID)

    # Install CLI
    Cli.install()
    Tns.disable_reporting()

    # Run Tests
    arguments = ['nosetests', '-v', '-s', '--nologcapture', '--with-doctest', '--with-xunit']
    for i in sys.argv:
        arguments.append(str(i))
    nose.run(argv=arguments)
