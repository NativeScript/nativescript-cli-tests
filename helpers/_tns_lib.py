'''
Wraper around tns commands
'''
import os
import shutil

from helpers._os_lib import run_aut, file_exists, extract_archive
from time import sleep

TNSPATH = os.path.join('node_modules', '.bin', 'tns')
NPATH = os.path.join('node_modules', '.bin', 'nativescript')
ANDROID_RUNTIME_PATH = "tns-android.tgz"
IOS_RUNTIME_PATH = "tns-ios.tgz"
ANDROID_RUNTIME_SYMLINK_PATH = os.path.join('tns-android', 'package')
IOS_RUNTIME_SYMLINK_PATH = os.path.join('tns-ios', 'package')

ANDROID_KEYSTORE_PATH = os.environ.get('ANDROID_KEYSTORE_PATH')
ANDROID_KEYSTORE_PASS = os.environ.get('ANDROID_KEYSTORE_PASS')
ANDROID_KEYSTORE_ALIAS = os.environ.get('ANDROID_KEYSTORE_ALIAS')
ANDROID_KEYSTORE_ALIAS_PASS = os.environ.get('ANDROID_KEYSTORE_ALIAS_PASS')


def install_cli(path_to_package=None):
    '''Install {N} CLI specified in CLI_PATH environment variable'''

    if 'CLI_PATH' in os.environ:
        location = os.path.join(os.environ['CLI_PATH'], "nativescript.tgz")
        shutil.copy2(
            location.strip(),
            (os.path.join(
                os.getcwd(),
                "nativescript.tgz")))
    if path_to_package is not None:
        shutil.copy2(
            path_to_package,
            (os.path.join(
                os.getcwd(),
                "nativescript.tgz")))

    output = run_aut("npm i nativescript.tgz")
    assert "ERR" "error" "FiberFuture" "dev-post-install" not in output, "{N} installation failed."
    assert file_exists("node_modules/.bin/tns"), "{N} installation failed."
    print output

def get_android_runtime():
    '''Copy android runtime form ANDROID_PATH to local folder'''

    if 'ANDROID_PATH' in os.environ:
        location = os.path.join(os.environ['ANDROID_PATH'], ANDROID_RUNTIME_PATH)
        shutil.copy2(
            location.strip(),
            (os.path.join(
                os.getcwd(),
                ANDROID_RUNTIME_PATH)))
    if file_exists(os.path.join(os.getcwd(), ANDROID_RUNTIME_PATH)):
        extract_archive(
            ANDROID_RUNTIME_PATH,
            os.path.splitext(ANDROID_RUNTIME_PATH)[0])

def get_ios_runtime():
    '''Copy android runtime form IOS_PATH to local folder'''

    if 'IOS_PATH' in os.environ:
        location = os.path.join(os.environ['IOS_PATH'], IOS_RUNTIME_PATH)
        shutil.copy2(
            location.strip(),
            (os.path.join(
                os.getcwd(),
                IOS_RUNTIME_PATH)))
    if file_exists(os.path.join(os.getcwd(), IOS_RUNTIME_PATH)):
        extract_archive(IOS_RUNTIME_PATH, os.path.splitext(IOS_RUNTIME_PATH)[0])

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, IOS_RUNTIME_SYMLINK_PATH))
        run_aut("npm install")
        os.chdir(current_dir)

def uninstall_cli():
    '''Uninstall local {N} installation'''

    output = run_aut("npm rm nativescript")
    print output

def create_project(proj_name, path=None, app_id=None, copy_from=None):
    '''Create {N} project'''

    # If --copy-from is not specified explicitly then project will copy
    # template-hello-world
    if copy_from is None:
        copy_from = "template-hello-world"

    command = TNSPATH + " create {0}".format(proj_name)

    if path is not None:
        command += " --path " + path
    if app_id is not None:
        command += " --appid " + app_id
    if copy_from is not None:
        command += " --copy-from " + copy_from

    output = run_aut(command)
    assert "Project {0} was successfully created".format(proj_name.replace("\"", "")) in output
    return output


def platform_add(platform=None, framework_path=None, path=None, symlink=False, assert_success=True):
    '''Add platform to {N} project'''

    command = TNSPATH + " platform add"

    if platform is not None:
        command += " {0}".format(platform)

    if framework_path is not None:
        command += " --frameworkPath {0}".format(framework_path)

    if path is not None:
        command += " --path {0}".format(path)

    if symlink is True:
        command += " --symlink"

    output = run_aut(command)

    if assert_success:
        assert "Copying template files..." in output
        assert "Project successfully created" in output

    return output


def prepare(path=None, platform=None, log_trace=False, assert_success=True):
    '''Prepare platform'''

    command = TNSPATH + " prepare"

    if platform is not None:
        command += " {0}".format(platform)

    if path is not None:
        command += " --path {0}".format(path)

    if log_trace:
        command += " --log trace"

    output = run_aut(command)

    if assert_success:
        assert "Project successfully prepared" in output

    return output


def library_add(platform=None, lib_path=None, path=None, assert_success=True):
    '''Add library'''

    command = TNSPATH + " library add"

    if platform is not None:
        command += " {0}".format(platform)

    if lib_path is not None:
        command += " {0}".format(lib_path)

    if path is not None:
        command += " --path {0}".format(path)

    output = run_aut(command)

    if assert_success:
        if platform is "android":
            assert "was successfully added for android platform" in output
        else:
            assert "The iOS Deployment Target is now 8.0 " + \
                "in order to support Cocoa Touch Frameworks." in output

    return output

def plugin_add(plugin=None, path=None, assert_success=True):
    '''Install {N} plugin'''

    command = TNSPATH + " plugin add"

    if plugin is not None:
        command += " {0}".format(plugin)

    if path is not None:
        command += " --path {0}".format(path)

    output = run_aut(command)

    if assert_success:
        assert "Successfully installed plugin {0}".format(plugin) in output

    return output

# C0301 - Line too long (%s/%s)
# R0913 - Too many arguments
# pylint: disable=C0301, R0913
def build(platform=None, mode=None, path=None, for_device=False, log_trace=False, assert_success=True):
    '''Build {N} project'''

    command = TNSPATH + " build"

    if platform is not None:
        command += " {0}".format(platform)

    if mode is not None:
        command += " --{0}".format(mode)

    if for_device:
        command += " --forDevice"

    if path is not None:
        command += " --path {0}".format(path)

    if log_trace:
        command += " --log trace"

    output = run_aut(command)

    if assert_success:
        assert "Project successfully prepared" in output
        if platform is "android":
            assert "BUILD SUCCESSFUL" in output
        else:
            assert "BUILD SUCCEEDED" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output

    return output


def run(platform=None, emulator=False, device=None, path=None, just_launch=True, assert_success=True):
    '''Run {N} project'''

    command = TNSPATH + " run"

    if platform is not None:
        command += " {0}".format(platform)

    if emulator:
        command += " --emulator"

    if device is not None:
        command += " --device {0}".format(device)

    if path is not None:
        command += " --path {0}".format(path)

    if just_launch:
        command += " --justlaunch"

    output = run_aut(command)

    if assert_success:
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        if platform is "android":
            assert "Successfully deployed on device with identifier" in output
        else:
            if emulator:
                assert "Session started without errors." in output
            else:
                assert "Successfully deployed on device" in output
                assert "Successfully run application org.nativescript." in output

    return output


def live_sync(platform=None, emulator=False, device=None, watch=False, path=None, assert_success=True):
    '''LiveSync {N} project'''

    command = TNSPATH + " livesync"

    if platform is not None:
        command += " {0}".format(platform)

    if emulator:
        command += " --emulator"

    if device is not None:
        command += " --device {0}".format(device)

    if watch:
        command += " --watch"

    if path is not None:
        command += " --path {0}".format(path)

    output = run_aut(command + " --log trace")

    if assert_success:
        assert "Project successfully prepared" in output
        if platform is "android":
            assert "Transferring project files..." in output
            assert "Successfully transferred all project files." in output
            assert "Applying changes..." in output
            assert "Successfully synced application org.nativescript." in output
            sleep(10)

    return output


def create_project_add_platform(proj_name, platform=None, framework_path=None, symlink=False):
    '''Create {N} project and platform'''
    create_project(proj_name)
    platform_add(platform, framework_path, proj_name, symlink)


def get_cli_version():
    '''Return {N} CLI version'''
    return run_aut(TNSPATH + " --version")
