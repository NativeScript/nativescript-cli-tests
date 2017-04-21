"""
Tests for building projects with the Android platform
"""
import os
import unittest
from zipfile import ZipFile

from core.base_class.BaseClass import BaseClass
from core.npm.npm import Npm
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_ALIAS_PASS, CURRENT_OS, \
    OSType, TEST_RUN_HOME
from core.settings.strings import *
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class BuildAndroidTests(BaseClass):
    app_name_dash = "test-app"
    app_name_space = "Test App"
    app_no_platform = "TestAppNoPlatform"

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)

        Folder.cleanup(cls.app_no_platform)

        File.remove(debug_apk)
        File.remove(release_apk)
        Folder.cleanup('temp')

        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        # Verify application state at the end of the test is correct
        if File.exists(self.app_name):
            data = TnsAsserts.get_package_json(self.app_name)
            assert "tns-android" in data[
                "nativescript"], "'tns-android' not found under `nativescript` inside package.json"
            assert "tns-android" not in data[
                "dependencies"], "'tns-android' found under `dependencies` inside package.json"

        BaseClass.tearDown(self)
        Folder.cleanup(self.platforms_android + '/build/outputs')

    @classmethod
    def tearDownClass(cls):
        File.remove(debug_apk)
        File.remove(release_apk)
        Folder.cleanup('temp')
        pass

    def test_001_build_android(self):
        # Default `tns run android`
        Tns.build_android(attributes={"--path": self.app_name})
        assert File.pattern_exists(self.platforms_android, "*.aar")
        assert not File.pattern_exists(self.platforms_android, "*.plist")
        assert not File.pattern_exists(self.platforms_android, "*.android.js")
        assert not File.pattern_exists(self.platforms_android, "*.ios.js")

        # And new platform specific file and verify next build is ok (test for issue #2697)
        src = os.path.join(self.app_name, 'app', 'app.js')
        dest_1 = os.path.join(self.app_name, 'app', 'new.android.js')
        dest_2 = os.path.join(self.app_name, 'app', 'new.ios.js')
        File.copy(src=src, dest=dest_1)
        File.copy(src=src, dest=dest_2)

        Tns.build_android(attributes={"--path": self.app_name})
        assert File.pattern_exists(self.platforms_android, "*.aar")
        assert not File.pattern_exists(self.platforms_android, "*.plist")
        assert not File.pattern_exists(self.platforms_android, "*.android.js")
        assert not File.pattern_exists(self.platforms_android, "*.ios.js")

        # Verify apk does not contain aar files
        archive = ZipFile(os.path.join(self.app_name, debug_apk_path))
        archive.extractall(self.app_name + "/temp")
        assert not File.pattern_exists(self.app_name + "/temp", "*.aar")
        assert not File.pattern_exists(self.app_name + "/temp", "*.plist")
        assert not File.pattern_exists(self.app_name + "/temp", "*.android.*")
        assert not File.pattern_exists(self.app_name + "/temp", "*.ios.*")

    def test_002_build_android_release(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": ""
                                      })

    def test_200_build_android_inside_project_folder(self):
        Folder.navigate_to(self.app_name)
        output = Tns.build_android(tns_path=os.path.join("..", TNS_PATH), attributes={"--path": self.app_name},
                                   assert_success=False)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert successfully_prepared in output
        assert build_successful in output
        assert successfully_built in output
        assert File.exists(os.path.join(self.app_name, debug_apk_path))

    def test_201_build_android_with_additional_prepare(self):
        """Verify that manually running prepare does not break next build command."""
        ReplaceHelper.replace(self.app_name, file_change=ReplaceHelper.CHANGE_JS)
        output = Tns.prepare_android(attributes={"--path": self.app_name}, assert_success=False)
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.INCREMENTAL)
        Tns.build_android(attributes={"--path": self.app_name})

    def test_202_build_android_with_log_trace_and_platform_not_added_or_empty(self):
        """'tns build android' with log trace options should output more logs."""
        Tns.create_app(self.app_no_platform)
        output = Tns.build_android(attributes={"--path": self.app_no_platform, "--log trace": ""})

        # Assert log trace show gradle logs
        assert "[DEBUG]" in output
        assert "FAILURE" not in output

    def test_301_build_project_with_dash_and_ios_inspector_added(self):
        """
        Verify we can build projects with dashes.
        Verify we can build android when inspector is added (test for CLI issue 2467)
        """
        Tns.create_app(self.app_name_dash)
        Tns.platform_add_android(attributes={"--path": self.app_name_dash, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Npm.install(package="tns-ios-inspector", option='--save-dev', folder=self.app_name_dash)
        Tns.build_android(attributes={"--path": self.app_name_dash})

        # Verify project id
        output = File.read(self.app_name_dash + "/package.json")
        assert app_identifier in output.lower()

        # Verify AndroidManifest.xml
        output = File.read(self.app_name_dash + "/platforms/android/src/main/AndroidManifest.xml")
        assert app_identifier in output.lower()

    def test_302_build_project_with_space(self):
        Tns.create_app(self.app_name_space)
        Tns.platform_add_android(attributes={"--path": "\"" + self.app_name_space + "\"",
                                             "--frameworkPath": ANDROID_RUNTIME_PATH})

        # Verify project builds
        Tns.build_android(attributes={"--path": "\"" + self.app_name_space + "\""})

        output = File.read(self.app_name_space + os.sep + "package.json")
        assert app_identifier in output.lower()

        output = File.read(self.app_name_space + "/platforms/android/src/main/AndroidManifest.xml")
        assert app_identifier in output.lower()

    def test_310_build_android_with_sdk22(self):
        # This is required when build with different SDK
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        Tns.build_android(attributes={"--compileSdk": "22", "--path": self.app_name})

    def test_311_build_android_with_sdk23(self):
        # This is required when build with different SDK
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        Tns.build_android(attributes={"--compileSdk": "23", "--path": self.app_name})

    def test_313_build_android_with_sdk99(self):
        # This is required when build with different SDK
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        output = Tns.build_android(attributes={"--compileSdk": "99", "--path": self.app_name},
                                   assert_success=False)
        assert "You have specified '99' for compile sdk, but it is not installed on your system." in output

    def test_321_build_with_copy_to_option(self):
        # TODO: Remove those lines after https://github.com/NativeScript/nativescript-cli/issues/2547 is fixed.
        # This is required when build with different SDK
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        File.remove(debug_apk)
        Tns.build_android(attributes={"--path": self.app_name, "--copy-to": "./"})
        assert File.exists(debug_apk)
        File.remove(debug_apk)

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "AppBuilder does not use Windows machines")
    def test_330_build_like_appbuilder(self):
        Folder.cleanup("temp")
        Folder.copy("data/apps/appbuilderProject", "temp/appbuilderProject")
        android_version = run("node -e \"console.log(require('./sut/tns-android/package/package.json').version)\"")

        # Init
        Folder.navigate_to("temp/appbuilderProject")
        output = Tns.run_tns_command("init", attributes={"--appid": "com.telerik.appbuilderProject",
                                                         "--frameworkName": "tns-android",
                                                         "--frameworkVersion": android_version,
                                                         "--path": "./appbuilderProject",
                                                         "--profile-dir": ".",
                                                         "--no-hooks": "",
                                                         "--ignoreScripts": ""
                                                         },
                                     tns_path="../../node_modules/.bin/tns")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert successfully_initialized in output

        # Update modules
        Folder.navigate_to("temp/appbuilderProject/appbuilderProject")
        uninstall_command = "npm uninstall tns-core-modules --save"
        run(uninstall_command)
        output = Tns.run_tns_command("plugin add tns-core-modules", tns_path="../../../node_modules/.bin/tns")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert installed_plugin.format(tns_core_modules) in output

        # Platform Add
        Folder.navigate_to("temp/appbuilderProject/appbuilderProject")

        output = Tns.run_tns_command("platform add android",
                                     attributes={"--frameworkPath": "../../../sut/tns-android/package",
                                                 "--profile-dir": "../",
                                                 "--no-hooks": "",
                                                 "--ignore-scripts": ""
                                                 },
                                     tns_path="../../../node_modules/.bin/tns")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert successfully_created in output

        # Build
        Folder.navigate_to("temp/appbuilderProject/appbuilderProject")
        output = Tns.run_tns_command("build android", attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                                                  "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                                                  "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                                                  "--keyStoreAliasPassword":
                                                                      ANDROID_KEYSTORE_ALIAS_PASS,
                                                                  "--sdk": "22",
                                                                  "--release": "",
                                                                  "--copy-to": "../appbuilderProject-debug.apk",
                                                                  "--profile-dir": "../",
                                                                  "--no-hooks": "",
                                                                  "--ignore-scripts": ""
                                                                  },
                                     tns_path="../../../node_modules/.bin/tns")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert successfully_built in output
        assert File.exists("temp/appbuilderProject/appbuilderProject-debug.apk")

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Skip on Windows, because tar is not available")
    def test_399_build_project_with_gz_file(self):
        # This is required when build with different SDK
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        # Create zip
        run("tar -czf " + self.app_name + "/app/app.tar.gz " + self.app_name + "/app/app.js")
        assert File.exists(self.app_name + "/app/app.tar.gz")
        # Build the project
        Tns.build_android(attributes={"--path": self.app_name})

    def test_400_build_with_no_platform(self):
        output = Tns.run_tns_command("build")
        assert invalid_input.format("build") in output
        assert "# build" in output

        if CURRENT_OS == OSType.OSX:
            assert "$ tns build <Platform>" in output
        else:
            assert "$ tns build android" in output

    def test_401_build_invalid_platform(self):
        output = Tns.run_tns_command("build invalidCommand")
        assert invalid_input.format("build") in output

    def test_402_build_no_path(self):
        output = Tns.run_tns_command("build android")
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_403_build_invalid_path(self):
        output = Tns.build_android(attributes={"--path": "invalidPath"}, assert_success=False)
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_404_build_invalid_option(self):
        output = Tns.build_android(attributes={"--" + invalid: "", "--path": self.app_name}, assert_success=False)
        assert invalid_option.format(invalid) in output

    @unittest.skipIf(CURRENT_OS == OSType.OSX, "Skip on OSX")
    def test_405_build_ios_on_linux_machine(self):
        output = Tns.build_ios(attributes={"--path": self.app_name}, assert_success=False)
        assert "Applications for platform ios can not be built on this OS" in output

    def test_406_build_release_without_key_options(self):
        output = Tns.build_android(attributes={"--release": "", "--path": self.app_name}, assert_success=False)
        assert "When producing a release build, you need to specify all --key-store-* options." in output
        assert "# build android" in output
        assert not File.exists(release_apk_path)
