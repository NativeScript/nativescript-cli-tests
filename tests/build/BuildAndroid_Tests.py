"""
Tests for building projects with the Android platform
"""
import os
import unittest
from zipfile import ZipFile

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_ALIAS_PASS, CURRENT_OS, \
    OSType, ANDROID_RUNTIME_SYMLINK_PATH, TEST_RUN_HOME
from core.tns.tns import Tns


class BuildAndroidTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)

        File.remove("TNSApp-debug.apk")
        File.remove("TNSApp-release.apk")
        Folder.cleanup('temp')

        Tns.create_app(BaseClass.app_name)
        Tns.platform_add_android(attributes={"--path": BaseClass.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_no_platform)
        Folder.cleanup(self.platforms_android + '/build/outputs')

    @classmethod
    def tearDownClass(cls):
        File.remove("TNSApp-debug.apk")
        File.remove("TNSApp-release.apk")
        Folder.cleanup(cls.app_name_dash)
        Folder.cleanup(cls.app_name_space)
        Folder.cleanup(cls.app_name_symlink)
        Folder.cleanup('temp')

    def test_001_build_android(self):
        Tns.build_android(attributes={"--path": self.app_name})

        assert File.exists(self.platforms_android + "/build/outputs/apk/TNSApp-debug.apk")
        assert File.pattern_exists(self.platforms_android, "*.aar")
        assert not File.pattern_exists(self.platforms_android, "*.plist")

        archive = ZipFile(self.platforms_android + "/build/outputs/apk/TNSApp-debug.apk")
        archive.extractall(self.app_name + "/temp")

        assert not File.pattern_exists(self.app_name + "/temp", "*.aar")

    def test_002_build_android_release(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": ""
                                      })
        assert File.exists(self.platforms_android + "/build/outputs/apk/TNSApp-release.apk")

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS,
                     "Ignore because of https://github.com/NativeScript/nativescript-cli/issues/282")
    def test_100_build_android_symlink(self):
        Tns.create_app(self.app_name_symlink)
        Tns.platform_add_android(attributes={"--path": self.app_name_symlink,
                                             "--frameworkPath": ANDROID_RUNTIME_SYMLINK_PATH,
                                             "--symlink": ""
                                             })
        Tns.build_android(attributes={"--path": self.app_name_symlink})

        # Verify build does not modify original manifest
        output = File.read(ANDROID_RUNTIME_SYMLINK_PATH + "/framework/src/main/AndroidManifest.xml")
        assert "__PACKAGE__" in output, "Build modify original AndroidManifest.xml, this is a problem!"
        assert "__APILEVEL__" in output, "Build modify original AndroidManifest.xml, this is a problem!"

    def test_200_build_android_inside_project_folder(self):
        Folder.navigate_to(self.app_name)
        output = Tns.build_android(tns_path=os.path.join("..", TNS_PATH), attributes={"--path": self.app_name},
                                   assert_success=False)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert File.exists(self.platforms_android + "/build/outputs/apk/TNSApp-debug.apk")

    def test_201_build_android_with_additional_prepare(self):
        Tns.prepare_android(attributes={"--path": self.app_name})
        Tns.build_android(attributes={"--path": self.app_name})
        assert File.exists(self.platforms_android + "/build/outputs/apk/TNSApp-debug.apk")

    def test_202_build_android_platform_not_added(self):
        Tns.create_app(self.app_no_platform)
        output = Tns.build_android(attributes={"--path": self.app_no_platform,
                                               "--log trace": ""
                                               })
        # Assert log trace show gradle logs
        assert "[DEBUG]" in output
        assert "FAILURE" not in output
        assert File.exists(self.app_no_platform + "/platforms/android/build/outputs/apk/TNSAppNoPlatform-debug.apk")

    def test_203_build_android_platform_when_platform_folder_is_empty(self):
        Tns.create_app(self.app_no_platform)
        Folder.cleanup(self.app_no_platform + '/platforms')
        output = Tns.build_android(attributes={"--path": self.app_no_platform, "--log trace": ""})

        # Assert log trace show gradle logs
        assert "[DEBUG]" in output
        assert "FAILURE" not in output
        assert File.exists(self.app_no_platform + "/platforms/android"
                                                  "/build/outputs/apk/TNSAppNoPlatform-debug.apk")

    def test_300_build_android_with_additional_styles_xml(self):
        # This is test for issue 644
        run("mkdir -p TestApp/app/App_Resources/Android/values")
        run("cp data/data/styles.xml TestApp/app/App_Resources/Android/values")
        Tns.build_android(attributes={"--path": self.app_name})
        assert File.exists(self.platforms_android + "/build/outputs/apk/TNSApp-debug.apk")

    def test_301_build_project_with_dash(self):
        Tns.create_app(self.app_name_dash)
        Tns.platform_add_android(attributes={"--path": self.app_name_dash,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.build_android(attributes={"--path": self.app_name_dash})
        assert File.exists(self.app_name_dash + "/platforms/android/build/outputs/apk/tnsapp-debug.apk")

        # Verify project id
        output = File.read(self.app_name_dash + "/package.json")
        assert "org.nativescript.tnsapp" in output

        # Verify AndroidManifest.xml
        output = File.read(self.app_name_dash + "/platforms/android/src/main/AndroidManifest.xml")
        assert "org.nativescript.tnsapp" in output

    def test_302_build_project_with_space(self):
        Tns.create_app(self.app_name_space)
        Tns.platform_add_android(attributes={"--path": "\"" + self.app_name_space + "\"",
                                             "--frameworkPath": ANDROID_RUNTIME_PATH})

        # Verify project build
        Tns.build_android(attributes={"--path": "\"" + self.app_name_space + "\""})
        assert File.exists(self.app_name_space + "/platforms/android/build/outputs/apk/TNSApp-debug.apk")

        output = File.read(self.app_name_space + os.sep + "package.json")
        assert "org.nativescript.TNSApp" in output

        output = File.read(self.app_name_space + "/platforms/android/src/main/AndroidManifest.xml")
        assert "org.nativescript.TNSApp" in output

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Skip on Windows, because tar is not available")
    def test_303_build_project_with_gz_file(self):
        # Create zip
        run("tar -czf " + self.app_name + "/app/app.tar.gz " + self.app_name + "/app/app.js")
        assert File.exists(self.app_name + "/app/app.tar.gz")
        # Build the project
        Tns.build_android(attributes={"--path": self.app_name})

    def test_310_build_android_with_sdk22(self):
        Folder.cleanup(self.app_name + '/platforms')
        Tns.build_android(attributes={"--compileSdk": "22", "--path": self.app_name})
        assert File.exists(self.app_name + "/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_311_build_android_with_sdk23(self):
        Folder.cleanup(self.app_name + '/platforms')
        Tns.build_android(attributes={"--compileSdk": "23", "--path": self.app_name})
        assert File.exists(self.platforms_android + "/build/outputs/apk/TNSApp-debug.apk")

    def test_313_build_android_with_sdk99(self):
        output = Tns.build_android(attributes={"--compileSdk": "99", "--path": self.app_name, "--log trace": ""},
                                   assert_success=False)
        assert "You have specified '99' for compile sdk, but it is not installed on your system." in output

    def test_320_build_release_with_copyto_option(self):
        Tns.platform_remove(platform="android", attributes={"--path": BaseClass.app_name}, assert_success=False)
        Folder.cleanup(self.app_name + '/platforms')
        Tns.platform_add_android(attributes={"--path": BaseClass.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--copy-to": "./",
                                      "--release": ""
                                      })
        assert File.exists(self.platforms_android + "/build/outputs/apk/TNSApp-release.apk")
        assert File.exists("TNSApp-release.apk")
        File.remove("TNSApp-release.apk")

    def test_321_build_with_copyto_option(self):
        Tns.build_android(attributes={"--path": self.app_name, "--copy-to": "./"})
        assert File.exists(self.platforms_android + "/build/outputs/apk/TNSApp-debug.apk")
        assert File.exists("TNSApp-debug.apk")
        File.remove("TNSApp-debug.apk")

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
        assert "Project successfully initialized." in output

        # Update modules
        Folder.navigate_to("temp/appbuilderProject/appbuilderProject")
        uninstall_command = "npm uninstall tns-core-modules --save"
        run(uninstall_command)
        output = Tns.run_tns_command("plugin add tns-core-modules", tns_path="../../../node_modules/.bin/tns")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert "Successfully installed plugin tns-core-modules" in output

        # Platform Add
        Folder.navigate_to("temp/appbuilderProject/appbuilderProject")

        output = Tns.run_tns_command("platform add android",
                                     attributes={"--frameworkPath": "../../../sut/tns-android/package",
                                                 "--profile-dir": "../",
                                                 "--no-hooks": "",
                                                 "--ignore-scripts": "",
                                                 "--symlink": ""
                                                 },
                                     tns_path="../../../node_modules/.bin/tns")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert "Project successfully created" in output

        # Prepare
        Folder.navigate_to("temp/appbuilderProject/appbuilderProject")
        output = Tns.run_tns_command("prepare android", attributes={"--profile-dir": "../",
                                                                    "--no-hooks": "",
                                                                    "--ignore-scripts": "",
                                                                    "--sdk": "22"
                                                                    },
                                     tns_path="../../../node_modules/.bin/tns")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert "Successfully prepared plugin tns-core-modules for android" in output
        assert "Successfully prepared plugin tns-core-modules-widgets for android" in output
        assert "Project successfully prepared" in output

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
        assert "Project successfully built" in output
        assert File.exists("temp/appbuilderProject/appbuilderProject-debug.apk")

    def test_400_build_with_no_platform(self):
        output = Tns.run_tns_command("build")
        assert "The input is not valid sub-command for 'build' command" in output
        assert "# build" in output

        if CURRENT_OS == OSType.OSX:
            assert "$ tns build <Platform>" in output
        else:
            assert "$ tns build android" in output

    def test_401_build_invalid_platform(self):
        output = Tns.run_tns_command("build invalidCommand")
        assert "The input is not valid sub-command for 'build' command" in output

    def test_402_build_no_path(self):
        output = Tns.run_tns_command("build android")
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_403_build_invalid_path(self):
        output = Tns.build_android(attributes={"--path": "invalidPath"}, assert_success=False)
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_404_build_invalid_option(self):
        output = Tns.build_android(attributes={"--invalidOption": "", "--path": self.app_name}, assert_success=False)
        assert "The option 'invalidOption' is not supported" in output

    @unittest.skipIf(CURRENT_OS == OSType.OSX, "Skip on OSX")
    def test_405_build_ios_on_linux_machine(self):
        output = Tns.build_ios(attributes={"--path": self.app_name}, assert_success=False)
        assert "Applications for platform ios can not be built on this OS" in output

    def test_406_build_release_without_key_options(self):
        output = Tns.build_android(attributes={"--release": "", "--path": self.app_name}, assert_success=False)
        assert "When producing a release build, you need to specify all --key-store-* options." in output
        assert "# build android" in output
        assert not File.exists(self.platforms_android + "/build/outputs/apk/TNSApp-release.apk")
