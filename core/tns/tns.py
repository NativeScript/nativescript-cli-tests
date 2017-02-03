"""
A wrapper of the tns commands.
"""

import os
import time

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, SUT_ROOT_FOLDER, DEVELOPMENT_TEAM, CLI_PATH, BRANCH, TEST_RUN_HOME
from core.xcode.xcode import Xcode


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
        if " " in path:
            path = "\"" + path + "\""
        if "release" in CLI_PATH.lower():  # TODO: Use Settings.BRANCH
            version = Tns.run_tns_command("", attributes={"--version": ""})
            Tns.plugin_remove("tns-core-modules", attributes={"--path": path}, assert_success=False)
            output = Tns.plugin_add("tns-core-modules@" + version, attributes={"--path": path}, assert_success=False)
            return output
        else:
            Tns.plugin_remove("tns-core-modules", attributes={"--path": path}, assert_success=False)
            output = Tns.plugin_add("tns-core-modules@next", attributes={"--path": path})
            return output

    @staticmethod
    def ensure_app_resources(path):
        app_resources_path = os.path.join(path, "app", "App_Resources")
        if File.exists(app_resources_path):
            pass
        else:
            print "AppResources not found. Will copy from default template..."
            src = os.path.join(TEST_RUN_HOME, "sut", "template-hello-world", "App_Resources")
            dest = os.path.join(TEST_RUN_HOME, path, "app", "App_Resources")
            Folder.copy(src, dest)

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
            attr = {"--template": SUT_ROOT_FOLDER + os.path.sep + "template-hello-world"}
        attr.update(attributes)
        if app_name is None:
            output = Tns.run_tns_command("create ", attributes=attr, log_trace=log_trace)
        else:
            output = Tns.run_tns_command("create \"" + app_name + "\"", attributes=attr, log_trace=log_trace)
        if assert_success:
            assert "nativescript-theme-core" in output
            assert "nativescript-dev-android-snapshot" in output
            assert "Project {0} was successfully created".format(app_name.replace("\"", "")) in output
        if update_modules:
            Tns.update_modules(path)
        Tns.ensure_app_resources(path)
        return output

    @staticmethod
    def create_app_ts(app_name, attributes={}, log_trace=False, assert_success=True, update_modules=True):
        attr = {"--template": "https://github.com/NativeScript/template-hello-world-ts.git#" + BRANCH}
        attributes.update(attr)
        output = Tns.create_app(app_name=app_name, attributes=attributes, log_trace=log_trace,
                                assert_success=assert_success,
                                update_modules=update_modules)
        if assert_success:
            assert "nativescript-dev-typescript" in output

            ts_config = os.path.join(app_name, "tsconfig.json")
            ref_dts = os.path.join(app_name, "references.d.ts")
            dts = os.path.join(app_name, "node_modules", "tns-core-modules", "tns-core-modules.d.ts")
            assert File.exists(ts_config)
            assert File.exists(dts)
            assert "./node_modules/tns-core-modules/tns-core-modules.d.ts" in File.read(ref_dts)

        return output

    @staticmethod
    def create_app_ng(app_name, attributes={}, log_trace=False, assert_success=True, update_modules=True):
        attr = {"--template": "https://github.com/NativeScript/template-hello-world-ng.git#" + BRANCH}
        attributes.update(attr)
        output = Tns.create_app(app_name=app_name, attributes=attributes, log_trace=log_trace, assert_success=assert_success,
                       update_modules=update_modules)
        if assert_success:
            assert "nativescript-angular" in output

        return output

    @staticmethod
    def platform_add(platform="", version=None, attributes={}, assert_success=True, log_trace=False, tns_path=None):
        if version is not None:
            platform += "@" + version
        output = Tns.run_tns_command("platform add " + platform, attributes=attributes, log_trace=log_trace,
                                     tns_path=tns_path)
        if assert_success:
            assert "Copying template files..." in output
            assert "Project successfully created." in output
        return output

    @staticmethod
    def platform_remove(platform="", attributes={}, assert_success=True, log_trace=False, tns_path=None):
        output = Tns.run_tns_command("platform remove " + platform, attributes=attributes, log_trace=log_trace,
                                     tns_path=tns_path)
        if assert_success:
            assert "Platform {0} successfully removed".format(platform) in output
            assert "error" not in output
        return output

    @staticmethod
    def platform_update(platform="", attributes={}, assert_success=True, log_trace=False, tns_path=None):
        output = Tns.run_tns_command("platform update " + platform, attributes=attributes, log_trace=log_trace,
                                     tns_path=tns_path)
        if assert_success:
            assert "Successfully updated to version" in output
        return output

    @staticmethod
    def platform_add_android(version=None, attributes={}, assert_success=True, log_trace=False, tns_path=None):
        return Tns.platform_add(platform="android", version=version, attributes=attributes,
                                assert_success=assert_success,
                                log_trace=log_trace,
                                tns_path=tns_path)

    @staticmethod
    def platform_add_ios(version=None, attributes={}, assert_success=True, log_trace=False, tns_path=None):
        return Tns.platform_add(platform="ios", version=version, attributes=attributes, assert_success=assert_success,
                                log_trace=log_trace,
                                tns_path=tns_path)

    @staticmethod
    def plugin_add(name, attributes={}, log_trace=False, assert_success=True):
        output = Tns.run_tns_command("plugin add " + name, attributes=attributes, log_trace=log_trace)
        if assert_success:
            assert "Successfully installed plugin {0}".format(name.replace("@next", "")) in output
        return output

    @staticmethod
    def plugin_remove(name, attributes={}, log_trace=False, assert_success=True):
        output = Tns.run_tns_command("plugin remove " + name, attributes=attributes, log_trace=log_trace)
        if assert_success:
            assert "Successfully removed plugin {0}".format(name.replace("@next", "")) in output
        return output

    @staticmethod
    def prepare_android(attributes={}, assert_success=True, log_trace=False, tns_path=None):
        output = Tns.run_tns_command("prepare android ", attributes=attributes, log_trace=log_trace, tns_path=tns_path)
        if assert_success:
            assert "Project successfully prepared" in output
        return output

    @staticmethod
    def prepare_ios(attributes={}, assert_success=True, log_trace=False, tns_path=None):
        output = Tns.run_tns_command("prepare ios ", attributes=attributes, log_trace=log_trace, tns_path=tns_path)
        if assert_success:
            assert "Project successfully prepared" in output
        return output

    @staticmethod
    def build_android(attributes={}, assert_success=True, tns_path=None):
        output = Tns.run_tns_command("build android", attributes=attributes, tns_path=tns_path)
        if assert_success:
            assert "BUILD SUCCESSFUL" in output
            assert "Project successfully built" in output
        return output

    @staticmethod
    def build_ios(attributes={}, assert_success=True, tns_path=None):
        if "8." in Xcode.get_version():
            # TODO: Use "--provision" instead.
            attr = {"--teamId": DEVELOPMENT_TEAM}
            attributes.update(attr)
        output = Tns.run_tns_command("build ios", attributes=attributes, tns_path=tns_path)
        if assert_success:
            assert "BUILD SUCCEEDED" in output
            assert "Project successfully built" in output
            assert "ERROR" not in output
        return output

    @staticmethod
    def deploy_android(attributes={}, assert_success=True, log_trace=False, timeout=None, tns_path=None):
        output = Tns.run_tns_command("deploy android", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                     tns_path=tns_path)
        if assert_success:
            assert "Project successfully built" in output
            assert "Successfully installed on device" in output
        return output

    @staticmethod
    def deploy_ios(attributes={}, assert_success=True, log_trace=False, timeout=None, tns_path=None):
        if "8." in Xcode.get_version():
            attr = {"--teamId": DEVELOPMENT_TEAM}
            attributes.update(attr)
        output = Tns.run_tns_command("deploy ios", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                     tns_path=tns_path)
        if assert_success:
            assert "Project successfully built" in output
            assert "Successfully installed on device" in output
        return output

    @staticmethod
    def run_android(attributes={}, assert_success=True, log_trace=False, timeout=None, tns_path=None):
        output = Tns.run_tns_command("run android", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                     tns_path=tns_path)
        if assert_success:
            assert "Project successfully built" in output
            assert "Successfully installed on device with identifier" in output
        return output

    @staticmethod
    def run_ios(attributes={}, assert_success=True, log_trace=False, timeout=None, tns_path=None):
        if "8." in Xcode.get_version():
            attr = {"--teamId": DEVELOPMENT_TEAM}
            attributes.update(attr)
        output = Tns.run_tns_command("run ios", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                     tns_path=tns_path)
        if assert_success:
            assert "Project successfully built" in output
            assert "Successfully installed on device with identifier" in output
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

    @staticmethod
    def init(attributes={}, assert_success=True, tns_path=None):
        output = Tns.run_tns_command("init", attributes=attributes, tns_path=tns_path)
        if assert_success:
            assert "Project successfully initialized" in output
        return output

    @staticmethod
    def install(attributes={}, assert_success=True, tns_path=None):
        output = Tns.run_tns_command("install", attributes=attributes, tns_path=tns_path)
        if assert_success:
            assert "Project successfully created" in output
        return output

    @staticmethod
    def disable_reporting():
        Tns.run_tns_command("usage-reporting disable")
        Tns.run_tns_command("error-reporting disable")
