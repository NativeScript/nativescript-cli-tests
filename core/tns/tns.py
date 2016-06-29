"""
A wrapper of the tns commands.
"""

import os
import time

from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, SUT_ROOT_FOLDER, TEST_RUN_HOME, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS


class Tns(object):
    @staticmethod
    def version():
        """
        Return {N} CLI version.
        """

        command = TNS_PATH + " --version"
        output = run(command)
        return output

    @staticmethod
    def create_app(app_name, path=None, app_id=None, copy_from=None, template=None, log_trace=False,
                   update_modules=True, assert_success=True):
        """
        Create {N} project.
        """

        command = TNS_PATH + " create {0}".format(app_name)

        if path is not None:
            command += " --path " + path

        if app_id is not None:
            command += " --appid " + app_id

        if template is None:
            # By default --copy-from template-hello-world
            if copy_from is not None:
                command += " --copy-from " + copy_from
            else:
                command += " --copy-from " + SUT_ROOT_FOLDER + os.path.sep + "template-hello-world"

        if template is not None:
            command += " --template " + template

        if log_trace:
            command += " --log trace"
        output = run(command)

        if update_modules:
            if path is not None:
                app_name = path + app_name
            Folder.navigate_to(app_name)
            npm_out1 = run("npm uninstall tns-core-modules")
            modules_path = SUT_ROOT_FOLDER + os.path.sep + "tns-core-modules.tgz"
            npm_out2 = run("npm install " + modules_path + " --save")
            Folder.navigate_to(os.path.join("node_modules", "tns-core-modules"))
            npm_out3 = run("npm uninstall tns-core-modules-widgets")
            widgets_path = SUT_ROOT_FOLDER + os.path.sep + "tns-core-modules-widgets.tgz"
            npm_out4 = run("npm install " + widgets_path + " --save")
            Folder.navigate_to(TEST_RUN_HOME, relative_from__current_folder=False)
            output = output + npm_out1 + npm_out2 + npm_out3 + npm_out4

        if assert_success:
            assert "Project {0} was successfully created".format(app_name.replace("\"", "")) in output
        return output

    @staticmethod
    def platform_add(platform=None, framework_path=None, path=None, symlink=False, log_trace=False):
        """
        Add target platform.
        """

        command = TNS_PATH + " platform add"

        if platform is not None:
            command += " {0}".format(platform)

        if framework_path is not None:
            command += " --framework-path {0}".format(framework_path)

        if path is not None:
            command += " --path {0}".format(path)

        if symlink is True:
            command += " --symlink"

        if log_trace:
            command += " --log trace"
        output = run(command)

        assert "Copying template files..." in output
        assert "Project successfully created." in output
        return output

    @staticmethod
    def prepare(platform=None, path=None, assert_success=True, log_trace=False, release=False):
        """
        Prepare target platform.
        """

        command = TNS_PATH + " prepare"

        if platform is not None:
            command += " {0}".format(platform)

        if path is not None:
            command += " --path {0}".format(path)

        if log_trace:
            command += " --log trace"

        if release is True:
            command += " --keyStorePath " + ANDROID_KEYSTORE_PATH + " --keyStorePassword " + ANDROID_KEYSTORE_PASS
            + " --keyStoreAlias " + ANDROID_KEYSTORE_ALIAS + " --keyStoreAliasPassword " + ANDROID_KEYSTORE_ALIAS_PASS
            + " --release"

        output = run(command)

        if assert_success:
            assert "Project successfully prepared" in output
        return output

    @staticmethod
    def plugin_add(plugin=None, path=None, assert_success=True):
        """
        Install {N} plugin.
        """

        command = TNS_PATH + " plugin add"

        if plugin is not None:
            command += " {0}".format(plugin)

        if path is not None:
            command += " --path {0}".format(path)

        # command += " --log trace"
        output = run(command)
        if assert_success:
            assert "Successfully installed plugin {0}".format(plugin) in output
        return output

    @staticmethod
    def build(platform=None, mode=None, for_device=False, path=None, release=False):
        """
        Build {N} project.
        """

        command = TNS_PATH + " build"

        if platform is not None:
            command += " {0}".format(platform)

        if mode is not None:
            command += " --{0}".format(mode)

        if for_device:
            command += " --for-device"

        if path is not None:
            command += " --path {0}".format(path)

        if release is True:
            command += " --keyStorePath " + ANDROID_KEYSTORE_PATH + " --keyStorePassword " + ANDROID_KEYSTORE_PASS
            + " --keyStoreAlias " + ANDROID_KEYSTORE_ALIAS + " --keyStoreAliasPassword " + ANDROID_KEYSTORE_ALIAS_PASS
            + " --release"

        output = run(command)

        assert "Project successfully prepared" in output
        if platform is "android":
            assert "BUILD SUCCESSFUL" in output
        elif platform is "ios":
            assert "BUILD SUCCEEDED" in output
        assert "Project successfully built" in output
        assert "ERROR" not in output
        return output

    @staticmethod
    def run(platform=None, emulator=False, device=None, path=None, assert_success=True):
        """
        Run {N} project.
        """

        command = TNS_PATH + " run"

        if platform is not None:
            command += " {0}".format(platform)

        if emulator:
            command += " --emulator"

        if device is not None:
            command += " --device {0}".format(device)

        if path is not None:
            command += " --path {0}".format(path)

        command += " --justlaunch --log trace"
        output = run(command)

        if assert_success:
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            if platform is "android":
                assert "Successfully deployed on device with identifier" in output
            elif platform is "ios":
                if emulator:
                    assert "Starting iOS Simulator" in output
                else:
                    assert "Successfully deployed on device" in output
                    assert "Successfully run application org.nativescript." in output
        return output

    @staticmethod
    def livesync(platform=None, emulator=False, device=None, path=None, assert_success=True):
        """
        The livesync command.

        Parameters:
            - android: --device, -- watch
            - iOS: --emulator, -- device, --watch
        """

        command = TNS_PATH + " livesync"

        if platform is not None:
            command += " {0}".format(platform)

        if emulator:
            command += " --emulator"

        if device is not None:
            command += " --device {0}".format(device)

        if path is not None:
            command += " --path {0}".format(path)

        command += " --justlaunch --log trace"
        output = run(command)

        if assert_success:
            assert "Project successfully prepared" in output
            if platform is "android":
                # assert "Start syncing application" in output
                # TODO: This is not longer avalable, uncomment if available again
                assert "Transferring project files..." in output
                assert "Successfully transferred all project files." in output
                assert "Applying changes..." in output
                assert "Successfully synced application" in output
                time.sleep(10)
            elif platform is "ios":
                assert "Project successfully prepared" in output
        return output

    @staticmethod
    def create_app_platform_add(app_name, platform=None, framework_path=None, symlink=False):
        """
        Create {N} project and add target platform.
        """

        Tns.create_app(app_name=app_name)
        Tns.platform_add(platform, framework_path, app_name, symlink)
