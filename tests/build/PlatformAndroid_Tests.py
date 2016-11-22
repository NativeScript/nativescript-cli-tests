"""
Test platform add (android)
"""
import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, CURRENT_OS, OSType, ANDROID_RUNTIME_PATH, ANDROID_RUNTIME_SYMLINK_PATH, \
    TEST_RUN_HOME
from core.tns.tns import Tns


class PlatformAndroidTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def test_001_platform_list_empty_project(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.run_tns_command("platform list", attributes={"--path": self.app_name})

        assert "No installed platforms found. Use $ tns platform add" in output
        if CURRENT_OS == OSType.OSX:
            assert "Available platforms for this OS:  ios and android" in output
        else:
            assert "Available platforms for this OS:  android" in output

    def test_002_platform_add_android(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name})

    def test_003_platform_add_android_framework_path(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

    def test_200_platform_list_inside_empty_project(self):
        Tns.create_app(self.app_name, update_modules=False)
        Folder.navigate_to(self.app_name)
        output = Tns.run_tns_command("platform list", tns_path=os.path.join("..", TNS_PATH))
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert "No installed platforms found. Use $ tns platform add" in output
        if CURRENT_OS == OSType.OSX:
            assert "Available platforms for this OS:  ios and android" in output
        else:
            assert "Available platforms for this OS:  android" in output

    def test_201_platform_add_android_inside_project(self):
        Tns.create_app(self.app_name, update_modules=False)
        Folder.navigate_to(self.app_name)
        output = Tns.platform_add_android(tns_path=os.path.join("..", TNS_PATH), assert_success=False)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert "Project successfully created" in output

    def test_202_platform_remove_android(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH})

        Tns.platform_remove(platform="android", attributes={"--path": self.app_name})
        assert Folder.is_empty(self.app_name + '/platforms')
        output = File.read(self.app_name + os.sep + "package.json")
        assert "tns-android" not in output

    def test_203_platform_add_android_custom_version(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(version="2.0.0", attributes={"--path": self.app_name})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"2.0.0\"" in output

    def test_204_platform_update_android(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(version="2.2.0", attributes={"--path": self.app_name})

        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"2.2.0\"" in output

        Tns.platform_update("android@2.3.0", attributes={"--path": self.app_name})
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"version\": \"2.3.0\"" in output

    def test_210_platform_update_android_patform_not_added(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_update("android", attributes={"--path": self.app_name}, assert_success=False)
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert not Folder.is_empty(self.app_name + "/platforms/android/build-tools/android-static-binding-generator")

    def test_220_set_sdk(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH,
                                             "--sdk": "19"})

        output = File.read(self.app_name + "/platforms/android/src/main/AndroidManifest.xml")
        assert "android:minSdkVersion=\"17\"" in output
        assert "android:targetSdkVersion=\"19\"" in output

    def test_300_platform_add_android_tagname(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(version="next", attributes={"--path": self.app_name})

    def test_301_set_sdk_not_installed(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_add_android(attributes={"--sdk": "29",
                                                      "--frameworkPath": ANDROID_RUNTIME_PATH,
                                                      "--path": self.app_name
                                                      })
        assert "Support for the selected Android target SDK android-29 is not verified. " + \
               "Your Android app might not work as expected." in output

        output = File.read(self.app_name + "/platforms/android/src/main/AndroidManifest.xml")
        assert "android:minSdkVersion=\"17\"" in output
        assert "android:targetSdkVersion=\"29\"/>" in output

    def test_400_platform_list_wrong_path(self):
        output = Tns.run_tns_command("platform list")
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_401_platform_list_wrong_path(self):
        output = Tns.run_tns_command("platform list", attributes={"--path": "invalidPath"})
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_420_platform_add_existing_platform(self):
        self.test_002_platform_add_android()
        output = Tns.platform_add_android(attributes={"--path ": self.app_name}, assert_success=False)
        assert "Platform android already added" in output

    def test_421_platform_add_android_wrong_framework_path(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_add_android(attributes={"--path": self.app_name,
                                                      "--frameworkPath": "invalidFile.tgz"
                                                      },
                                          assert_success=False)
        assert "no such package available" in output
        assert "invalidFile.tgz" in output

    def test_423_platform_add_android_wrong_framework_path_option(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_add_android(attributes={"--path": self.app_name,
                                                      "--frameworkpath": "tns-android.tgz"
                                                      },
                                          assert_success=False)
        assert "The option 'frameworkpath' is not supported." in output

    def test_425_platform_add_empty_platform(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_add(attributes={"--path": self.app_name}, assert_success=False)
        assert "No platform specified. Please specify a platform to add" in output
        assert "Usage" in output

    def test_430_platform_remove_missing_platform(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_remove(platform="android", attributes={"--path": self.app_name}, assert_success=False)
        assert "The platform android is not added to this project"
        assert "Usage" in output

    def test_431_platform_remove_invalid_platform(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_remove("invalidPlatform", attributes={"--path": self.app_name}, assert_success=False)
        assert "Invalid platform invalidplatform. Valid platforms are ios or android." in output
        assert "Usage" in output

    def test_432_platform_remove_empty_platform(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_remove(attributes={"--path": self.app_name}, assert_success=False)
        assert "No platform specified. Please specify a platform to remove" in output
        assert "Usage" in output

    def test_441_platform_update_invalid_platform(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name})
        output = Tns.platform_update("invalidPlatform", attributes={"--path": self.app_name}, assert_success=False)
        assert "Invalid platform invalidplatform. Valid platforms are ios or android." in output
        assert "Usage" in output

    def test_442_platform_update_empty_platform(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_update(attributes={"--path": self.app_name}, assert_success=False)
        assert "1mNo platform specified. Please specify platforms to update" in output
        assert "Usage" in output
