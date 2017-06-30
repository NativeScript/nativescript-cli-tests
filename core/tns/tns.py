"""
A wrapper of tns commands.
"""
import os
import time

from core.npm.npm import Npm
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.osutils.process import Process
from core.settings.settings import TNS_PATH, SUT_FOLDER, DEVELOPMENT_TEAM, BRANCH, TEST_RUN_HOME, \
    COMMAND_TIMEOUT, CURRENT_OS
from core.settings.strings import config_release, codesign, config_debug
from core.tns.tns_platform_type import Platform
from core.tns.tns_verifications import TnsAsserts
from core.xcode.xcode import Xcode


class Tns(object):
    NEXT_TAG = 'next'  # npm tag used when we publish master branch of tns-core-modules

    @staticmethod
    def __get_platform_string(platform=Platform.NONE):
        if platform is Platform.NONE:
            return ""
        if platform is Platform.ANDROID:
            return "android"
        if platform is Platform.IOS:
            return "ios"
        return platform

    @staticmethod
    def __get_final_package_name(app_name, platform=Platform.NONE):
        """
        Get base name of final package (without extension and `-debug`, `-release` strings).
        :param app_name: Folder where application is located.
        :param platform: Platform (ANDROID or IOS)
        :return:
        """

        # Android respect id in package.json
        # iOS respect folder name
        # See https://github.com/NativeScript/nativescript-cli/issues/2575

        if platform is Platform.ANDROID:
            app_id = Tns.get_app_id(app_name)
            # We can't get last with [-1] because some apps have wrong format of id.
            # For example: `org.nativescript.demo.barcodescanner`
            # In this case we should retrun `demo` as final package name.
            return app_id.split('.')[2]
        elif platform is Platform.IOS:
            return app_name.replace(" ", "").replace("-", "").replace("_", "").replace("\"", "")
        else:
            raise "Invalid platform!"

    @staticmethod
    def __get_app_name_from_attributes(attributes={}):
        app_name = ""
        for k, v in attributes.iteritems():
            if k == "--path":
                app_name = v
        return app_name

    @staticmethod
    def version(tns_path=None):
        """
        Get version of locally installed CLI
        :return: Version of the CLI as string
        """
        return Tns.run_tns_command("", attributes={"--version": ""}, tns_path=tns_path).split(os.linesep)[-1]

    @staticmethod
    def kill():
        """
        Kill all running `tns` processes
        """
        Process.kill(proc_name='node', proc_cmdline='tns')  # Stop 'node' to kill the livesync after each test method.

    @staticmethod
    def get_app_id(app_name):
        """
        Get application id from package.json
        :param app_name: Folder where application is located.
        :return: Application id.
        """
        json = TnsAsserts.get_package_json(app_name)
        return json.get('nativescript').get('id')

    @staticmethod
    def run_tns_command(command, tns_path=None, attributes={}, log_trace=False, timeout=COMMAND_TIMEOUT, wait=True):
        cmd = TNS_PATH + " " + command
        if tns_path is not None:
            cmd = tns_path + " " + command
        if len(attributes) != 0:
            for k, v in attributes.iteritems():
                cmd += " " + k + " " + v
        if log_trace:
            cmd += " --log trace"
        print cmd
        output = run(command=cmd, timeout=timeout, wait=wait)
        return output

    @staticmethod
    def update_modules(path, tns_path=None):
        """
        Update modules for {N} project
        :param path: Path to {N} project
        :param tns_path: Path to tns executable
        :return: Output of command that update tns-core-modules plugin.
        """

        # Escape path with spaces
        if " " in path:
            path = "\"" + path + "\""

        # In release branch we get modules versions from MODULES_VERSION variable.
        # To prevent errors in local testing when it is not specified default value is set to be same as CLI version.
        if "release" in BRANCH.lower():
            cli_version = Tns.version(tns_path=None)
            version = os.environ.get("MODULES_VERSION", cli_version)
            Tns.plugin_remove("tns-core-modules", attributes={"--path": path}, assert_success=False, tns_path=tns_path)
            output = Tns.plugin_add("tns-core-modules@" + version, attributes={"--path": path}, assert_success=False,
                                    tns_path=tns_path)
        # In master branch we use @next packages.
        else:
            Tns.plugin_remove("tns-core-modules", attributes={"--path": path}, assert_success=False, tns_path=tns_path)
            output = Tns.plugin_add("tns-core-modules@" + Tns.NEXT_TAG, attributes={"--path": path}, tns_path=tns_path)
        assert "undefined" not in output, "Something went wrong when modules are installed."
        assert "ERR" not in output, "Something went wrong when modules are installed."
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
    def create_app(app_name, attributes={}, log_trace=False, assert_success=True, update_modules=True,
                   force_clean=True):

        if force_clean:
            if File.exists(app_name):
                Folder.cleanup(app_name)

        path = app_name
        attributes_to_string = ""
        for k, v in attributes.iteritems():
            if "--path" in k:
                path = v
            attributes_to_string = "".join("{0} {1}".format(k, v))
        attr = {}
        if not any(s in attributes_to_string for s in ("--ng", "--template", "--tsc")):
            attr = {"--template": SUT_FOLDER + os.path.sep + "tns-template-hello-world.tgz"}
        attr.update(attributes)
        if app_name is None:
            output = Tns.run_tns_command("create ", attributes=attr, log_trace=log_trace)
        else:
            output = Tns.run_tns_command("create \"" + app_name + "\"", attributes=attr, log_trace=log_trace)
        if assert_success:
            TnsAsserts.created(app_name=app_name, output=output)
        if update_modules:
            Tns.update_modules(path)
        Tns.ensure_app_resources(path)
        return output

    @staticmethod
    def create_app_ts(app_name, attributes={}, log_trace=False, assert_success=True, update_modules=True):
        """
        Create TypeScript application based on hello-world-ts template in GitHub (branch is respected)
        :param app_name: Application name.
        :param attributes: Additional attributes for `tns create` command.
        :param log_trace: If true runs with `--log trace`.
        :param assert_success: If true application is verified once it is created.
        :param update_modules: If true update modules (branch is respected).
        :return: output of `tns create command`
        """
        attr = {"--template": SUT_FOLDER + os.path.sep + "tns-template-hello-world-ts.tgz"}
        attributes.update(attr)
        output = Tns.create_app(app_name=app_name, attributes=attributes, log_trace=log_trace,
                                assert_success=assert_success,
                                update_modules=update_modules)
        if assert_success:
            TnsAsserts.created_ts(app_name=app_name, output=output)
        return output

    @staticmethod
    def create_app_ng(app_name, attributes={}, log_trace=False, assert_success=True, update_modules=True,
                      template_version=None):
        if template_version is not None:
            template = "tns-template-hello-world-ng@" + template_version
            attr = {"--template": template}
        else:
            attr = {"--template": SUT_FOLDER + os.path.sep + "tns-template-hello-world-ng.tgz"}
        attributes.update(attr)
        output = Tns.create_app(app_name=app_name, attributes=attributes, log_trace=log_trace,
                                assert_success=assert_success,
                                update_modules=update_modules)
        if assert_success:
            if Npm.version() < 5:
                assert "nativescript-angular" in output
            assert File.exists(os.path.join(app_name, 'node_modules', 'nativescript-theme-core'))

        return output

    @staticmethod
    def platform_add(platform=Platform.NONE, version=None, attributes={}, assert_success=True, log_trace=False,
                     tns_path=None):

        #######################################################################################
        # Add platforms
        #######################################################################################

        platform_string = Tns.__get_platform_string(platform)

        if version is not None:
            platform_string = platform_string + "@" + version

        output = Tns.run_tns_command("platform add " + platform_string, attributes=attributes, log_trace=log_trace,
                                     tns_path=tns_path)

        #######################################################################################
        # Verify platforms added (if assert_success=True)
        #######################################################################################

        app_name = Tns.__get_app_name_from_attributes(attributes)
        if assert_success:
            TnsAsserts.platform_added(app_name=app_name, platform=platform, output=output)
        return output

    @staticmethod
    def platform_remove(platform=Platform.NONE, attributes={}, assert_success=True, log_trace=False, tns_path=None):
        platform_string = Tns.__get_platform_string(platform)
        output = Tns.run_tns_command("platform remove " + platform_string, attributes=attributes, log_trace=log_trace,
                                     tns_path=tns_path)

        app_name = Tns.__get_app_name_from_attributes(attributes)
        if assert_success:
            assert "Platform {0} successfully removed".format(platform_string) in output
            assert "error" not in output
            if platform is Platform.ANDROID:
                assert not File.exists(app_name + TnsAsserts.PLATFORM_ANDROID)
            if platform is Platform.IOS:
                assert not File.exists(app_name + TnsAsserts.PLATFORM_IOS)
        return output

    @staticmethod
    def platform_clean(platform=Platform.NONE, attributes={}, assert_success=True, log_trace=False, tns_path=None):
        platform_string = Tns.__get_platform_string(platform)
        output = Tns.run_tns_command("platform clean " + platform_string, attributes=attributes, log_trace=log_trace,
                                     tns_path=tns_path)

        app_name = Tns.__get_app_name_from_attributes(attributes)
        if assert_success:
            assert "Platform {0} successfully removed".format(platform_string) in output
            assert "error" not in output
            if platform is Platform.ANDROID:
                assert File.exists(app_name + TnsAsserts.PLATFORM_ANDROID)
            if platform is Platform.IOS:
                assert File.exists(app_name + TnsAsserts.PLATFORM_IOS)
            assert "Project successfully created" in output
        return output

    @staticmethod
    def platform_update(platform=Platform.NONE, version=None, attributes={}, assert_success=True, log_trace=False,
                        tns_path=None):
        platform_string = Tns.__get_platform_string(platform)
        if version is not None:
            platform_string = platform_string + "@" + version
        output = Tns.run_tns_command("platform update " + platform_string, attributes=attributes, log_trace=log_trace,
                                     tns_path=tns_path)
        if assert_success:
            assert "Successfully updated to version" in output, "Failed to update platform. Log: " + output
        return output

    @staticmethod
    def platform_add_android(version=None, attributes={}, assert_success=True, log_trace=False, tns_path=None):
        return Tns.platform_add(platform=Platform.ANDROID, version=version, attributes=attributes,
                                assert_success=assert_success,
                                log_trace=log_trace,
                                tns_path=tns_path)

    @staticmethod
    def platform_add_ios(version=None, attributes={}, assert_success=True, log_trace=False, tns_path=None):
        return Tns.platform_add(Platform.IOS, version=version, attributes=attributes, assert_success=assert_success,
                                log_trace=log_trace,
                                tns_path=tns_path)

    @staticmethod
    def platform_list(attributes={}, log_trace=False, tns_path=None):
        return Tns.run_tns_command("platform list", attributes=attributes, log_trace=log_trace, tns_path=tns_path)

    @staticmethod
    def plugin_add(name, attributes={}, log_trace=False, assert_success=True, tns_path=None):
        output = Tns.run_tns_command("plugin add " + name, attributes=attributes, log_trace=log_trace,
                                     tns_path=tns_path)
        if assert_success:
            assert "Successfully installed plugin {0}".format(name.replace("@" + Tns.NEXT_TAG, "")) in output
        return output

    @staticmethod
    def plugin_remove(name, attributes={}, log_trace=False, assert_success=True, tns_path=None):
        output = Tns.run_tns_command("plugin remove " + name, attributes=attributes, log_trace=log_trace,
                                     tns_path=tns_path)
        if assert_success:
            assert "Successfully removed plugin {0}".format(name.replace("@" + Tns.NEXT_TAG, "")) in output
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
            assert "BUILD SUCCESSFUL" in output, "Build failed!"
            assert "Project successfully built" in output, "Build failed!"
            assert "NOT FOUND" not in output  # Test for https://github.com/NativeScript/android-runtime/issues/390
            app_name = Tns.__get_app_name_from_attributes(attributes=attributes)
            apk_base_name = Tns.__get_final_package_name(app_name, platform=Platform.ANDROID)
            base_app_path = app_name + TnsAsserts.PLATFORM_ANDROID + "build/outputs/apk/" + apk_base_name
            if "--release" in attributes.keys():
                apk_path = base_app_path + "-release.apk"
            else:
                apk_path = base_app_path + "-debug.apk"
            apk_path = apk_path.replace("\"", "")  # Handle projects with space
            assert File.exists(apk_path), "Apk file does not exist at " + apk_path
        return output

    @staticmethod
    def build_ios(attributes={}, assert_success=True, tns_path=None):
        if "7." in Xcode.get_version():
            print "Xcode 7. No need to pass --teamId param!"
        else:
            attr = {"--teamId": DEVELOPMENT_TEAM}
            attributes.update(attr)
        output = Tns.run_tns_command("build ios", attributes=attributes, tns_path=tns_path)
        if assert_success:
            assert "BUILD SUCCEEDED" in output
            assert "Project successfully built" in output
            assert "ERROR" not in output
            assert "malformed" not in output
            assert codesign in output
            app_name = Tns.__get_app_name_from_attributes(attributes=attributes)
            app_id = Tns.__get_final_package_name(app_name, platform=Platform.IOS)
            app_name = app_name.replace("\"", "")  # Handle projects with space

            # Verify release/debug builds
            if "--release" in attributes.keys():
                assert config_release in output
            else:
                assert config_debug in output

            entitlements_path = app_name + '/platforms/ios/' + app_id + '/' + app_id + '.entitlements'
            assert File.exists(entitlements_path), "Entitlements file is missing!"
            assert 'dict' in File.read(entitlements_path), "Entitlements file content is wrong!"

            # Verify simulator/device builds
            device_folder = app_name + "/platforms/ios/build/device/"
            emu_folder = app_name + "/platforms/ios/build/emulator/"
            if "--forDevice" in attributes.keys() or "--for-device" in attributes.keys():
                assert "build/device/" + app_id + ".app" in output
                assert File.exists(device_folder + app_id + ".ipa"), "IPA file not found!"
                bundle_content = File.read(device_folder + app_id + ".app/" + app_id)
            else:
                assert "build/emulator/" + app_id + ".app" in output
                assert File.exists(app_name + "/platforms/ios/" + app_id + "/" + app_id + "-Prefix.pch")
                assert File.exists(emu_folder + app_id + ".app")
                bundle_content = File.read(emu_folder + app_id + ".app/" + app_id)
            if "--release" in attributes.keys():
                assert "TKLiveSync" not in bundle_content, "TKLiveSync binaries available in release configuration."
            else:
                assert "TKLiveSync" in bundle_content, "TKLiveSync binaries not available in debug configuration."
        return output

    @staticmethod
    def deploy_android(attributes={}, assert_success=True, log_trace=False, timeout=COMMAND_TIMEOUT, tns_path=None):
        output = Tns.run_tns_command("deploy android", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                     tns_path=tns_path)
        if assert_success:
            assert "Project successfully built" in output
            assert "Successfully installed on device" in output
        return output

    @staticmethod
    def deploy_ios(attributes={}, assert_success=True, log_trace=False, timeout=COMMAND_TIMEOUT, tns_path=None):
        if "7." in Xcode.get_version():
            print "Xcode 7. No need to pass --teamId param!"
        else:
            attr = {"--teamId": DEVELOPMENT_TEAM}
            attributes.update(attr)
        output = Tns.run_tns_command("deploy ios", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                     tns_path=tns_path)
        if assert_success:
            assert "Project successfully built" in output
            assert "Successfully installed on device" in output
        return output

    @staticmethod
    def run_android(attributes={}, assert_success=True, log_trace=False, timeout=COMMAND_TIMEOUT, tns_path=None,
                    wait=True):
        output = Tns.run_tns_command("run android", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                     tns_path=tns_path, wait=wait)
        if assert_success:
            assert "Project successfully built" in output
            assert "Successfully installed on device with identifier" in output
            app_name = Tns.__get_app_name_from_attributes(attributes=attributes)
            apk_base_name = Tns.__get_final_package_name(app_name, platform=Platform.ANDROID)
            base_app_path = app_name + TnsAsserts.PLATFORM_ANDROID + "build/outputs/apk/" + apk_base_name
            if "--release" in attributes.keys():
                apk_path = base_app_path + "-release.apk"
            else:
                apk_path = base_app_path + "-debug.apk"
            apk_path = apk_path.replace("\"", "")  # Handle projects with space
            assert File.exists(apk_path), "Apk file does not exist at " + apk_path
        return output

    @staticmethod
    def run_ios(attributes={}, assert_success=True, log_trace=False, timeout=COMMAND_TIMEOUT, tns_path=None, wait=True):
        if "7." in Xcode.get_version():
            print "Xcode 7. No need to pass --teamId param!"
        else:
            attr = {"--teamId": DEVELOPMENT_TEAM}
            attributes.update(attr)
        output = Tns.run_tns_command("run ios", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                     tns_path=tns_path, wait=wait)
        if assert_success:
            assert "Project successfully built" in output
            assert "Successfully installed on device with identifier" in output
        return output

    @staticmethod
    def debug_android(attributes={}, log_trace=False, timeout=COMMAND_TIMEOUT, tns_path=None):
        log_file = Tns.run_tns_command("debug android", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                       tns_path=tns_path, wait=False)
        return log_file

    @staticmethod
    def debug_ios(attributes={}, log_trace=False, timeout=COMMAND_TIMEOUT, tns_path=None):
        log_file = Tns.run_tns_command("debug ios", attributes=attributes, log_trace=log_trace, timeout=timeout,
                                       tns_path=tns_path, wait=False)
        return log_file

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

    @staticmethod
    def wait_for_log(log_file, string_list, not_existing_string_list=None, timeout=30, check_interval=3,
                     clean_log=True):
        """
        Wait until log file contains list of string.
        :param log_file: Path to log file.
        :param string_list: List of strings.
        :param not_existing_string_list: List of string that should not be in logs.
        :param timeout: Timeout.
        :param check_interval: Check interval.
        :param clean_log: Specify if content of log file should be delete after check.
        """
        t_end = time.time() + timeout
        all_items_found = False
        not_found_list = []
        log = ""
        while time.time() < t_end:
            not_found_list = []
            log = File.read(log_file)
            for item in string_list:
                if item in log:
                    print "'{0}' found.".format(item)
                else:
                    not_found_list.append(item)
            if not_found_list == []:
                all_items_found = True
                print "Log contains: {0}".format(string_list)
                break
            else:
                print "'{0}' NOT found. Wait...".format(not_found_list)
                time.sleep(check_interval)
            if 'BUILD FAILED' in log:
                print 'BUILD FAILED. No need to wait more time!'
                break
            if 'Unable to sync files' in log:
                print 'Sync process failed. No need to wait more time!'
                break
            if 'errors were thrown' in log:
                print 'Multiple errors were thrown. No need to wait more time!'
                break

        if clean_log and (CURRENT_OS is not OSType.WINDOWS) and all_items_found:
            File.write(file_path=log_file, text="")

        if all_items_found:
            if not_existing_string_list is None:
                pass
            else:
                for item in not_existing_string_list:
                    assert item not in log, "{0} found! It should not be in logs.".format(item)
        else:
            print "##### OUTPUT BEGIN #####\n"
            print log
            print "##### OUTPUT END #####\n"
            print ""
            assert False, "Output does not contain {0}".format(not_found_list)
