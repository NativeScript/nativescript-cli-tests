"""
Test platform add (android)
"""
import os
import unittest
from time import sleep

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, CURRENT_OS, OSType, ANDROID_RUNTIME_PATH, ANDROID_RUNTIME_SYMLINK_PATH, \
    TEST_RUN_HOME
from core.tns.tns import Tns


class PlatformAndroid(unittest.TestCase):
    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        pass

    def test_001_platform_list_empty_project(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " platform list --path TNS_App")

        assert "No installed platforms found. Use $ tns platform add" in output
        if CURRENT_OS == OSType.OSX:
            assert "Available platforms for this OS:  ios and android" in output
        else:
            assert "Available platforms for this OS:  android" in output

    def test_002_platform_add_android(self):
        Tns.create_app(app_name="TNS_App")
        output = Tns.platform_add(platform="android", path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output
        if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
            assert File.list_of_files_exists(
                    'TNS_App/platforms/android',
                    'platform_android_current.txt')

    def test_003_platform_add_android_framework_path(self):
        Tns.create_app(app_name="TNS_App")
        output = Tns.platform_add(
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH,
                path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output
        if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
            assert File.list_of_files_exists(
                    'TNS_App/platforms/android',
                    'platform_android_current.txt')

    def test_004_platform_add_android_symlink_and_frameworkPath(self):
        if CURRENT_OS == OSType.WINDOWS:
            print "Ignore because of https://github.com/NativeScript/nativescript-cli/issues/282"
        else:
            Tns.create_app(app_name="TNS_App")
            output = Tns.platform_add(
                    platform="android",
                    path="TNS_App",
                    framework_path=ANDROID_RUNTIME_SYMLINK_PATH,
                    symlink=True)
            assert "Copying template files..." in output
            assert "Project successfully created" in output

            if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
                assert File.list_of_files_exists(
                        'TNS_App/platforms/android',
                        'platform_android_symlink.txt')

    def test_200_platform_list_inside_empty_project(self):
        Tns.create_app(app_name="TNS_App")
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(os.path.join("..", TNS_PATH) + " platform list")
        os.chdir(current_dir)

        assert "No installed platforms found. Use $ tns platform add" in output
        if CURRENT_OS == OSType.OSX:
            assert "Available platforms for this OS:  ios and android" in output
        else:
            assert "Available platforms for this OS:  android" in output

    def test_201_platform_add_android_inside_project(self):
        Tns.create_app(app_name="TNS_App")
        Folder.navigate_to("TNS_App")
        output = run(os.path.join("..", TNS_PATH) + " platform add android")
        Folder.navigate_to(TEST_RUN_HOME)

        assert "Copying template files..." in output
        assert "Project successfully created" in output
        if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
            assert File.list_of_files_exists(
                    'TNS_App/platforms/android',
                    'platform_android_current.txt')

    def test_202_platform_remove_android(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)

        output = run(TNS_PATH + " platform remove android --path TNS_App")
        assert "Platform android successfully removed." in output

        assert not "error" in output
        assert Folder.is_empty('TNS_App/platforms')

        output = run("cat TNS_App/package.json")
        assert not "tns-android" in output

    def test_203_platform_add_android_custom_version(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android@1.3.0")
        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.3.0\"" in output

        if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
            assert File.list_of_files_exists(
                    'TNS_App/platforms/android',
                    'platform_android_1.3.0.txt')

    @unittest.skip("1.3.0 do not support older versions, enable after 1.3.1 is released")
    def test_204_platform_update_android(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android@1.1.0")
        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.1.0\"" in output

        command = TNS_PATH + " platform update android@1.2.0 --path TNS_App"
        output = run(command)
        assert "Successfully updated to version  1.2.0" in output

        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.2.0\"" in output
        if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
            assert File.list_of_files_exists(
                    'TNS_App/platforms/android',
                    'platform_android_1.2.0.txt')
        Tns.build(platform="android", path="TNS_App")

    @unittest.skip("Now it fails, need to fix the test.")
    def test_205_platform_update_android_to_same_version(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="android")
        output = run(TNS_PATH + " platform update android --path TNS_App")
        assert "Current and new version are the same." in output
        assert "Usage" in output
        Tns.build(platform="android", path="TNS_App")

    @unittest.skip("1.3.0 do not support older versions, enable after 1.3.1 is released")
    def test_206_platform_downgrade_android_to_old_version(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android@1.2.0")
        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.2.0\"" in output

        #         Comment these lines as they cause the test to fail
        #         since commits in master on July 27, 2015
        #         [31;1mCannot read property 'substring' of undefined[0m
        #         TypeError: Cannot read property 'substring' of undefined

        #         command = TNS_PATH + " platform update android@1.1.0 --path TNS_App"
        #         output = emulate(command + " < y_key.txt")
        #         assert "You are going to downgrade to android runtime v.1.1.0. Are you sure?" in output
        #         assert "Successfully updated to version  1.1.0" in output

        os.system(
                TNS_PATH +
                " platform update android@1.1.0 --path TNS_App < y_key.txt")
        sleep(10)

        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.1.0\"" in output
        Tns.build(platform="android", path="TNS_App")

    @unittest.skip(
            "Execute when platform update command starts respecting --frameworkPath.")
    def test_207_platform_update_android_to_latest_version(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android@1.0.0")
        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.0.0\"" in output

        command = TNS_PATH + " platform update android --frameworkPath {0} --path TNS_App".format(ANDROID_RUNTIME_PATH)
        output = run(command)
        assert "Successfully updated to version" in output
        Tns.build(platform="android", path="TNS_App")

    @unittest.skip(
            "Skiped because of https://github.com/NativeScript/nativescript-cli/issues/784")
    def test_208_platform_downgrade_android_from_latest_version(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)

        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1." in output

        #         Comment these lines as they cause the test to fail
        #         since commits in master on July 27, 2015
        #         [31;1mCannot read property 'substring' of undefined[0m
        #         TypeError: Cannot read property 'substring' of undefined

        #         command = TNS_PATH + " platform update android@1.0.0 --path TNS_App"
        #         output = emulate(command + " < y_key.txt")
        #         assert "You are going to downgrade to android runtime v.1.0.0. Are you sure?" in output
        #         assert "Successfully updated to version  1.0.0" in output

        os.system(
                TNS_PATH +
                " platform update android@1.1.0 --path TNS_App < y_key.txt")
        sleep(10)

        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.1.0\"" in output
        Tns.build(platform="android", path="TNS_App")

    def test_210_platform_update_android_patform_not_added(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " platform update android --path TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert not Folder.is_empty(
                "TNS_App/platforms/android/build-tools/android-static-binding-generator")

    def test_220_set_sdk(self):
        Tns.create_app(app_name="TNS_App")
        Tns.platform_add(
                platform="android --sdk 19",
                framework_path=ANDROID_RUNTIME_PATH,
                path="TNS_App")

        output = run(
                "cat TNS_App/platforms/android/src/main/AndroidManifest.xml ")
        assert "android:minSdkVersion=\"17\"" in output
        assert "android:targetSdkVersion=\"19\"" in output

    def test_300_platform_add_android_tagname(self):
        Tns.create_app(app_name="TNS_App")
        output = Tns.platform_add(platform="android@next", path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output

    def test_221_set_sdk_not_installed(self):
        Tns.create_app(app_name="TNS_App")
        output = Tns.platform_add(
                platform="android --sdk 29",
                framework_path=ANDROID_RUNTIME_PATH,
                path="TNS_App")
        assert "Support for the selected Android target SDK android-29 is not verified. " + \
               "Your Android app might not work as expected." in output

        output = run(
                "cat TNS_App/platforms/android/src/main/AndroidManifest.xml")
        assert "android:minSdkVersion=\"17\"" in output
        assert "android:targetSdkVersion=\"29\"/>" in output

    def test_400_platform_list_wrong_path(self):
        output = run(TNS_PATH + " platform list")
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_401_platform_list_wrong_path(self):
        output = run(TNS_PATH + " platform list --path invalidPath")
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_420_platform_add_existing_platform(self):
        self.test_002_platform_add_android()

        output = run(TNS_PATH + " platform add android --path TNS_App")
        assert "Platform android already added" in output

    def test_421_platform_add_android_wrong_framework_path(self):
        Tns.create_app(app_name="TNS_App")
        output = run(
                TNS_PATH +
                " platform add android --frameworkPath invalidFile.tgz --path TNS_App")
        assert "Error: no such package available" in output
        assert "invalidFile.tgz" in output

    def test_423_platform_add_android_wrong_framework_path_option(self):
        Tns.create_app(app_name="TNS_App")
        output = run(
                TNS_PATH +
                " platform add android --frameworkpath tns-android.tgz --path TNS_App")
        assert "The option 'frameworkpath' is not supported." in output

    def test_424_platform_add_android_wrong_symlink_option(self):
        Tns.create_app(app_name="TNS_App")
        output = run(
                TNS_PATH +
                " platform add android --frameworkPath tns-android.tgz --simlink --path TNS_App")
        assert "The option 'simlink' is not supported." in output

    def test_425_platform_add_empty_platform(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " platform add --path TNS_App")
        assert "No platform specified. Please specify a platform to add" in output
        assert "Usage" in output

    def test_430_platform_remove_missing_platform(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " platform remove android --path TNS_App")
        assert "The platform android is not added to this project. " + \
               "Please use 'tns platform add <platform>'" in output
        assert "Usage" in output

    def test_431_platform_remove_invalid_platform(self):
        Tns.create_app(app_name="TNS_App")
        output = run(
                TNS_PATH +
                " platform remove invalidPlatform --path TNS_App")
        assert "Invalid platform invalidplatform. Valid platforms are ios or android." in output
        assert "Usage" in output

    def test_432_platform_remove_empty_platform(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " platform remove --path TNS_App")
        assert "No platform specified. Please specify a platform to remove" in output
        assert "Usage" in output

    def test_441_platform_update_invalid_platform(self):
        Tns.create_app(app_name="TNS_App")
        output = run(
                TNS_PATH +
                " platform update invalidPlatform --path TNS_App")
        assert "Invalid platform invalidplatform. Valid platforms are ios or android." in output
        assert "Usage" in output

    def test_442_platform_update_empty_platform(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " platform update --path TNS_App")
        assert "1mNo platform specified. Please specify platforms to update" in output
        assert "Usage" in output
