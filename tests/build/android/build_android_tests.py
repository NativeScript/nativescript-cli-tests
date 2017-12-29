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
from core.osutils.expected_platform_files import ExpectedPlatformsFiles


class BuildAndroidTests(BaseClass):
    debug_apk = "TestApp-debug.apk"
    release_apk = "TestApp-release.apk"

    app_ts_name = "TestAppTS"
    app_name_dash = "test-app"
    app_name_space = "Test App"
    app_no_platform = "TestAppNoPlatform"
    platforms_android = BaseClass.app_name + "/" + TnsAsserts.PLATFORM_ANDROID

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

        Folder.cleanup(cls.app_no_platform)

        File.remove(cls.debug_apk)
        File.remove(cls.release_apk)
        Folder.cleanup('temp')

        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        # Add release and debug configs
        debug = os.path.join(cls.app_name, 'app', 'config.debug.json')
        release = os.path.join(cls.app_name, 'app', 'config.release.json')
        File.write(file_path=debug, text='{"config":"debug"}')
        File.write(file_path=release, text='{"config":"release"}')

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        # Verify application state at the end of the test is correct
        if File.exists(self.app_name):
            data = TnsAsserts.get_package_json(self.app_name)
            assert "tns-android" in data["nativescript"], "'tns-android' not found under `nativescript` in package.json"
            assert "tns-android" not in data["dependencies"], "'tns-android' found under `dependencies` in package.json"

        BaseClass.tearDown(self)
        Folder.cleanup(self.platforms_android + '/build/outputs')
        Folder.cleanup("with space")

    @classmethod
    def tearDownClass(cls):
        File.remove(cls.debug_apk)
        File.remove(cls.release_apk)
        Folder.cleanup('temp')
        pass

    def test_001_build_android(self):
        Tns.build_android(attributes={"--path": self.app_name})
        assert File.pattern_exists(self.platforms_android, "*.aar")
        assert not File.pattern_exists(self.platforms_android, "*.plist")
        assert not File.pattern_exists(self.platforms_android, "*.android.js")
        assert not File.pattern_exists(self.platforms_android, "*.ios.js")

        # Compares folders and files names in platforms/android.
        # Ignores files that changes part of their name in every build.
        ignore_files = set([os.path.join('build', 'android-profile', 'profile-*'),
                            os.path.join('app', 'build', 'intermediates', 'pre-dexed', 'debug', 'classes*'),
                            os.path.join('.*', '.DS_Store')])
        assert Folder.has_same_structure(os.path.join(Folder.get_current_folder(), self.platforms_android),
                                         ExpectedPlatformsFiles.ANDROID, ignore_files)

        # Configs are respected
        assert 'debug' in File.read(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH, 'config.json'))

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
        archive = ZipFile(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, self.debug_apk))
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
                                      }, log_trace=True)

        # Configs are respected
        assert 'release' in File.read(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH, 'config.json'))
        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, self.release_apk))

    def test_200_build_android_inside_project_folder(self):
        Folder.navigate_to(self.app_name)
        output = Tns.build_android(tns_path=os.path.join("..", TNS_PATH), attributes={"--path": self.app_name},
                                   assert_success=False, log_trace=True)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert successfully_prepared in output
        assert build_successful in output
        assert successfully_built in output
        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, self.debug_apk))

    def test_201_build_android_with_additional_prepare(self):
        """Verify that manually running prepare does not break next build command."""
        ReplaceHelper.replace(self.app_name, file_change=ReplaceHelper.CHANGE_JS)
        output = Tns.prepare_android(attributes={"--path": self.app_name}, assert_success=False)
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.INCREMENTAL)
        Tns.build_android(attributes={"--path": self.app_name})

    @unittest.skip("Skip this test until we release tns-android@3.4.0")
    def test_202_build_android_with_log_trace_and_platform_not_added_or_empty(self):
        """'tns build android' with log trace options should output more logs."""
        Tns.create_app(self.app_no_platform)
        output = Tns.build_android(attributes={"--path": self.app_no_platform}, log_trace=True)

        # Assert log trace show gradle logs
        assert "[DEBUG]" in output
        assert "FAILURE" not in output

    def test_300_build_android_with_scoped_dependencies(self):
        """
        'tns build android' with scoped dependencies.
        Test for:
        https://github.com/telerik/nativescript-ui-feedback/issues/191
        https://github.com/NativeScript/nativescript-cli/pull/2837
        """

        # Simulate scoped dependency
        Npm.install(package="nativescript-telerik-ui-pro", option="--save", folder=self.app_name)
        File.replace(file_path=os.path.join(self.app_name, 'package.json'),
                     str1='"nativescript-telerik-ui-pro"',
                     str2='"@progress/nativescript-telerik-ui-pro"')
        path1 = os.path.join(self.app_name, 'node_modules', 'nativescript-telerik-ui-pro')
        path2 = os.path.join(self.app_name, 'node_modules', '@progress', 'nativescript-telerik-ui-pro')
        Folder.copy(src=path1, dst=path2)
        Folder.cleanup(folder=os.path.join(self.app_name, 'node_modules', 'nativescript-telerik-ui-pro'))
        File.replace(file_path=os.path.join(self.app_name, 'node_modules', '@progress', 'nativescript-telerik-ui-pro',
                                            'package.json'),
                     str1='"name": "nativescript-telerik-ui-pro",',
                     str2='"name": "progress@nativescript-telerik-ui-pro",')

        # Build android
        output = Tns.build_android(attributes={"--path": self.app_name})
        assert "Flavor 'nativescript-telerik-ui' has unknown dimension 'nativescript-telerik-ui'" not in output

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
        output = File.read(self.app_name_dash + "/" + TnsAsserts.PLATFORM_ANDROID_SRC_MAIN_PATH + "AndroidManifest.xml")
        assert app_identifier in output.lower()

    def test_302_build_project_with_space(self):
        Tns.create_app(self.app_name_space)
        Tns.platform_add_android(
            attributes={"--path": "\"" + self.app_name_space + "\"", "--frameworkPath": ANDROID_RUNTIME_PATH})

        # Ensure ANDROID_KEYSTORE_PATH contain spaces (verification for CLI issue 2650)
        Folder.create("with space")
        base_path, file_name = os.path.split(ANDROID_KEYSTORE_PATH)
        cert_with_space_path = os.path.join("with space", file_name)
        File.copy(src=ANDROID_KEYSTORE_PATH, dest=cert_with_space_path)

        # Verify project builds
        Tns.build_android(attributes={"--path": "\"" + self.app_name_space + "\"",
                                      "--keyStorePath": "\"" + cert_with_space_path + "\"",
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": ""
                                      })

        output = File.read(self.app_name_space + os.sep + "package.json")
        assert app_identifier in output.lower()

        output = File.read(
            self.app_name_space + "/" + TnsAsserts.PLATFORM_ANDROID_SRC_MAIN_PATH + "AndroidManifest.xml")
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

        File.remove(self.debug_apk)
        Tns.build_android(attributes={"--path": self.app_name, "--copy-to": "./"})
        assert File.exists(self.debug_apk)
        File.remove(self.debug_apk)

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

    def test_390_build_project_with_foursquare_android_oauth(self):
        # This is required when build with different SDK
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        # Add foursquare native library as dependency
        source = os.path.join('data', 'issues', 'android-runtime-755', 'app.gradle')
        target = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'app.gradle')
        File.copy(src=source, dest=target)

        # Build the project
        output = Tns.build_android(attributes={"--path": self.app_name}, assert_success=False)
        assert ':asbg:generateBindings', 'Static Binding Generator not executed'
        assert 'cannot access its superclass' not in output

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
        assert "applications for platform ios can not be built on this os" in output.lower()

    def test_406_build_release_without_key_options(self):
        output = Tns.build_android(attributes={"--release": "", "--path": self.app_name}, assert_success=False)
        assert "When producing a release build, you need to specify all --key-store-* options." in output
        assert "# build android" in output
        assert not File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_PATH, self.release_apk))

    def test_440_binding_text_exists(self):
        # https: // github.com / NativeScript / android - runtime / issues / 833
        Tns.create_app_ts(self.app_ts_name)

        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        Folder.cleanup(os.path.join(self.app_name, 'app'))
        copy = os.path.join(self.app_ts_name, 'app')
        paste = self.app_name
        Folder.move(copy, paste)

        Tns.build_android(attributes={"--path": self.app_name})
        bindings_path = os.path.join(self.app_name, 'platforms', 'android', 'build-tools', 'sbg-bindings.txt')
        binding = os.stat(bindings_path)
        assert binding.st_size > 15000
        print binding.st_size
        Folder.cleanup(self.app_ts_name)
