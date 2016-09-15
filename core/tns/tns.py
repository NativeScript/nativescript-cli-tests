"""
A wrapper of the tns commands.
"""

import os
import time

from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, SUT_ROOT_FOLDER, TEST_RUN_HOME


class Tns(object):
    @staticmethod
    def run_tns_command(command, tns_path=None, attributes={}, log_trace=False, timeout=None):
        cmd = TNS_PATH + " " + command
        if tns_path is not None:
            cmd = tns_path + " " + command
        if len(attributes) != 0:
            for k, v in attributes.iteritems():
                cmd += " " + k + " " + v
        if log_trace:
            cmd += " --log trace"
        print cmd
        if timeout is not None:
            output = run(cmd, timeout)
        else:
            output = run(cmd)
        return output

    @staticmethod
    def update_modules(path):
        Folder.navigate_to(path)
        npm_out1 = run("npm uninstall tns-core-modules")
        modules_path = SUT_ROOT_FOLDER + os.path.sep + "tns-core-modules.tgz"
        npm_out2 = run("npm install " + modules_path + " --save")
        Folder.navigate_to(os.path.join("node_modules", "tns-core-modules"))
        npm_out3 = run("npm uninstall tns-core-modules-widgets")
        widgets_path = SUT_ROOT_FOLDER + os.path.sep + "tns-core-modules-widgets.tgz"
        npm_out4 = run("npm install " + widgets_path + " --save")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        output = npm_out1 + npm_out2 + npm_out3 + npm_out4
        return output

    @staticmethod
    def create_app(app_name, attributes={}, log_trace=False, assert_success=True, update_modules=True):
        path = app_name
        attributes_to_string = ""
        for k, v in attributes.iteritems():
            if "--path" in k:
                path = v
            attributes_to_string = "".join("{0} {1}".format(k, v))
        attr = {}
        if not any(s in attributes_to_string for s in ("--ng", "--template", "--tsc")):
            attr = {"--copy-from": SUT_ROOT_FOLDER + os.path.sep + "template-hello-world"}
        attr.update(attributes)
        if app_name is None:
            output = Tns.run_tns_command("create ", attributes=attr, log_trace=log_trace)
        else:
            output = Tns.run_tns_command("create \"" + app_name + "\"", attributes=attr, log_trace=log_trace)
        if assert_success:
            assert "Project {0} was successfully created".format(app_name.replace("\"", "")) in output
        if update_modules:
            Tns.update_modules(path)
        return output

    @staticmethod
    def platform_add_android(version=None, attributes={}, assert_success=True, log_trace=False):
        platform = "android"
        if version is not None:
            platform += "@" + version
        output = Tns.run_tns_command("platform add " + platform, attributes=attributes, log_trace=log_trace)
        if assert_success:
            assert "Copying template files..." in output
            assert "Project successfully created." in output
        return output

    @staticmethod
    def platform_add_ios(version=None, attributes={}, log_trace=False):
        platform = "ios"
        if version is not None:
            platform += "@" + version
        output = Tns.run_tns_command("platform add " + platform, attributes=attributes, log_trace=log_trace)
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        return output

    @staticmethod
    def plugin_add(name, attributes={}, log_trace=False, assert_success=True):
        output = Tns.run_tns_command("plugin add " + name, attributes=attributes, log_trace=log_trace)
        if assert_success:
            assert "Successfully installed plugin {0}".format(name) in output
        return output

    @staticmethod
    def prepare_android(attributes={}, assert_success=True, log_trace=False):
        output = Tns.run_tns_command("prepare android ", attributes=attributes, log_trace=log_trace)
        if assert_success:
            assert "Project successfully prepared" in output
        return output

    @staticmethod
    def prepare_ios(attributes={}, assert_success=True, log_trace=False):
        output = Tns.run_tns_command("prepare ios ", attributes=attributes, log_trace=log_trace)
        if assert_success:
            assert "Project successfully prepared" in output
        return output

    @staticmethod
    def build_android(attributes={}, assert_success=True):
        output = Tns.run_tns_command("build android", attributes=attributes)
        if assert_success:
            assert "Project successfully prepared" in output
            assert "BUILD SUCCESSFUL" in output
            assert "Project successfully built" in output
        return output

    @staticmethod
    def build_ios(attributes={}, assert_success=True):
        output = Tns.run_tns_command("build ios", attributes=attributes)
        if assert_success:
            assert "Project successfully prepared" in output
            assert "BUILD SUCCEEDED" in output
            assert "Project successfully built" in output
            assert "ERROR" not in output
        return output

    @staticmethod
    def run_android(attributes={}, assert_success=True, log_trace=False, timeout=None):
        output = Tns.run_tns_command("run android", attributes=attributes, log_trace=log_trace, timeout=timeout)
        if assert_success:
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device with identifier" in output
        return output

    @staticmethod
    def run_ios(attributes={}, assert_success=True, log_trace=False, timeout=None):
        output = Tns.run_tns_command("run ios", attributes=attributes, log_trace=log_trace, timeout=timeout)
        if assert_success:
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            if "emulator" in attributes.iteritems():
                assert "Starting iOS Simulator" in output
            else:
                assert "Successfully deployed on device" in output
                assert "Successfully run application org.nativescript." in output
        return output

    @staticmethod
    def livesync(platform=None, attributes={}, log_trace=True, assert_success=True):
        command = "livesync "
        if platform is not None:
            command += platform
        attributes.update({"--justlaunch": ""})
        output = Tns.run_tns_command(command, attributes=attributes, log_trace=log_trace)

        if assert_success:
            assert "Project successfully prepared" in output
            if platform is "android":
                assert "Transferring project files..." in output
                assert "Applying changes..." in output
                assert "Successfully synced application" in output
                time.sleep(10)
            elif platform is "ios":
                assert "Project successfully prepared" in output
        return output


