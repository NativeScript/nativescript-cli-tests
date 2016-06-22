"""
Test platform add (ios)
"""
import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, IOS_RUNTIME_SYMLINK_PATH, ANDROID_RUNTIME_PATH, IOS_RUNTIME_PATH, \
    CURRENT_OS, OSType
from core.tns.tns import Tns


class PlatformiOS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if CURRENT_OS != OSType.OSX:
            raise NameError("Can not run iOS tests on non OSX OS.")

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        pass

    def test_001_platform_list_ios_project(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios",
                                    framework_path=IOS_RUNTIME_SYMLINK_PATH, symlink=True)
        output = run(TNS_PATH + " platform list --path TNS_App")
        assert "The project is not prepared for any platform" in output
        assert "Installed platforms:  ios" in output

        Tns.prepare(path="TNS_App", platform="ios")
        output = run(TNS_PATH + " platform list --path TNS_App")
        assert "The project is prepared for:  ios" in output
        assert "Installed platforms:  ios" in output

        Tns.platform_add(
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH,
                path="TNS_App",
                symlink=True)
        output = run(TNS_PATH + " platform list --path TNS_App")
        assert "The project is prepared for:  ios" in output
        assert "Installed platforms:  android and ios" in output

        Tns.prepare(path="TNS_App", platform="android")
        output = run(TNS_PATH + " platform list --path TNS_App")
        assert "The project is prepared for:  ios and android" in output
        assert "Installed platforms:  android and ios" in output

    def test_002_platform_add_ios(self):
        Tns.create_app(app_name="TNS_App")
        output = Tns.platform_add(platform="ios", path="TNS_App", symlink=False)
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        # TODO: Fix files in platform_ios_current.txt
        #if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
        #    assert File.list_of_files_exists(
        #            'TNS_App/platforms/ios',
        #            'platform_ios_current.txt')
        #Tns.build(platform="ios", path="TNS_App")

    def test_003_platform_add_ios_symlink_and_framework_path(self):
        Tns.create_app(app_name="TNS_App")
        output = Tns.platform_add(
                platform="ios",
                path="TNS_App",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        # if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
        #     assert File.list_of_files_exists(
        #             'TNS_App/platforms/ios',
        #             'platform_ios_symlink.txt')

        # Verify Runtime is symlink
        output = run("ls -la TNS_App/platforms/ios/")
        assert "internal ->" in output
        assert "package/framework/internal" in output

    def test_200_platform_add_ios_framework_path(self):
        Tns.create_app(app_name="TNS_App")
        output = Tns.platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_PATH,
                path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        # if ('TEST_RUN' in os.environ) and (
        #             "SMOKE" not in os.environ['TEST_RUN']):
        #     assert File.list_of_files_exists(
        #             'TNS_App/platforms/ios',
        #             'platform_ios_current.txt')

        # If project.xcworkspace is there Xcode project name is wrong
        assert not File.exists(
                "TNS_App/platforms/ios/TNSApp.xcodeproj/project.xcworkspace")

    def test_201_platform_remove_ios(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_PATH)

        output = run(TNS_PATH + " platform remove ios --path TNS_App")
        assert "Platform ios successfully removed." in output

        assert "error" not in output
        assert Folder.is_empty('TNS_App/platforms')

        output = run("cat TNS_App/package.json")
        assert "tns-ios" not in output

    def test_202_platform_remove_ios_symlink(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        output = run(TNS_PATH + " platform remove ios --path TNS_App")
        assert "Platform ios successfully removed." in output

        assert "error" not in output
        assert Folder.is_empty('TNS_App/platforms')

        output = run("cat TNS_App/package.json")
        assert "tns-ios" not in output

    def test_300_platform_add_ios_custom_version(self):
        Tns.create_app(app_name="TNS_App")
        output = Tns.platform_add(platform="ios@1.4.0", path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.4.0\"" in output

        if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
            assert File.list_of_files_exists(
                    'TNS_App/platforms/ios',
                    'platform_ios_1.4.0.txt')
        Tns.build(platform="ios", path="TNS_App")

    @unittest.skip(
            "Skip until fixed: https://github.com/NativeScript/nativescript-cli/issues/772")
    def test_301_platform_update_ios(self):
        Tns.create_app(app_name="TNS_App")
        output = Tns.platform_add(platform="ios@1.2.2", path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.2.2\"" in output

        command = TNS_PATH + " platform update ios@1.3.0 --path TNS_App < enter_key.txt"
        run("echo " + command)
        os.system(command)

        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.3.0\"" in output

        if ('TEST_RUN' in os.environ) and ("SMOKE" not in os.environ['TEST_RUN']):
            assert File.list_of_files_exists(
                    'TNS_App/platforms/ios',
                    'platform_ios_1.3.0.txt')
        Tns.build(platform="ios", path="TNS_App")

    @unittest.skip("This test fails on the build machine because " +
                   "it needs more time to update ios@1.1.0. " +
                   "Try to execute update command again with run_aut or add time.sleep(x).")
    def test_302_platform_downgrade_ios_to_old_version(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios@1.2.0")
        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.2.0\"" in output

        command = TNS_PATH + " platform update ios@1.1.0 --path TNS_App < enter_key.txt"
        run("echo " + command)
        os.system(command)

        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.1.0\"" in output
        Tns.build(platform="ios", path="TNS_App")

    @unittest.skip("Ignored because of https://github.com/NativeScript/nativescript-cli/issues/743")
    def test_303_platform_update_ios_to_latest_version(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios@1.0.0")
        output = run("cat TNS_App/package.json")
        assert "\"version\": \"1.0.0\"" in output

        command = TNS_PATH + " platform update ios --frameworkPath {0} --path TNS_App".format(IOS_RUNTIME_PATH)

        output = run(command)
        assert "We need to override xcodeproj file. The old one will be saved at" in output

        # output = emulate("echo '' | " + TNS_PATH + " platform update")
        assert "Successfully updated to version  1.2.0" in output
        Tns.build(platform="ios", path="TNS_App")


@unittest.skip(
        "Skip until fixed: https://github.com/NativeScript/nativescript-cli/issues/772")
def test_304_platform_downgrade_ios_from_latest_version(self):
    Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_PATH)

    output = run("cat TNS_App/package.json")
    assert "\"version\": \"1." in output

    command = TNS_PATH + " platform update ios@1.1.0 --path TNS_App < enter_key.txt"
    run("echo " + command)
    os.system(command)

    output = run("cat TNS_App/package.json")
    assert "\"version\": \"1.1.0\"" in output
    Tns.build(platform="ios", path="TNS_App")


def test_310_platform_add_ios_custom_experimental_version(self):
    Tns.create_app(app_name="TNS_App")
    output = Tns.platform_add(platform="ios@0.9.2-exp-ios-8.2", path="TNS_App")
    assert "Copying template files..." in output
    assert "Project successfully created" in output

    output = run("cat TNS_App/package.json")
    assert "\"version\": \"0.9.2-exp-ios-8.2\"" in output


def test_320_platform_add_ios_custom_bundle_id(self):
    # Create project with different appId
    Tns.create_app(app_name="TNS_App", app_id="org.nativescript.MyApp")
    output = run("cat TNS_App/package.json")
    assert "\"id\": \"org.nativescript.MyApp\"" in output

    # Add iOS platform
    output = Tns.platform_add(
            platform="ios",
            path="TNS_App",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
    assert "Project successfully created" in output

    # Verify plist file in native project (after prepare)
    Tns.prepare(path="TNS_App", platform="ios")
    output = run("cat TNS_App/platforms/ios/TNSApp/TNSApp-Info.plist")
    assert "org.nativescript.MyApp" in output


def test_330_platform_update_ios_patform_not_added(self):
    Tns.create_app(app_name="TNS_App")
    output = run(TNS_PATH + " platform update ios --path TNS_App")
    assert "Copying template files..." in output
    assert "Project successfully created." in output
    assert not Folder.is_empty("TNS_App/platforms/ios/internal/metadata-generator")


def test_400_platform_add_existing_platform(self):
    self.test_004_platform_add_ios_symlink_and_framework_path()

    output = run(TNS_PATH + " platform add ios --path TNS_App")
    assert "Platform ios already added" in output
    assert "Usage" in output
