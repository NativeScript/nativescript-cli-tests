'''
Test platform add (ios)
'''
import unittest
import os

from helpers._os_lib import run_aut, cleanup_folder, check_file_exists, \
    is_empty, file_exists
from helpers._tns_lib import TNSPATH, ANDROID_RUNTIME_PATH, build, \
    create_project, create_project_add_platform, IOS_RUNTIME_PATH, IOS_RUNTIME_SYMLINK_PATH, \
    platform_add, prepare

# pylint: disable=R0201, C0111


class PlatformiOS(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_Platform_List_IOS_Project(self):
        create_project_add_platform(proj_name="TNS_App", platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH, symlink=True)
        output = run_aut(TNSPATH + " platform list --path TNS_App")
        assert "The project is not prepared for any platform" in output
        assert "Installed platforms:  ios" in output

        prepare(path="TNS_App", platform="ios")
        output = run_aut(TNSPATH + " platform list --path TNS_App")
        assert "The project is prepared for:  ios" in output
        assert "Installed platforms:  ios" in output

        platform_add(
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH,
            path="TNS_App",
            symlink=True)
        output = run_aut(TNSPATH + " platform list --path TNS_App")
        assert "The project is prepared for:  ios" in output
        assert "Installed platforms:  android and ios" in output

        prepare(path="TNS_App", platform="android")
        output = run_aut(TNSPATH + " platform list --path TNS_App")
        assert "The project is prepared for:  ios and android" in output
        assert "Installed platforms:  android and ios" in output

    def test_002_Platform_Add_iOS(self):
        create_project(proj_name="TNS_App")
        output = platform_add(platform="ios", path="TNS_App", symlink=False)
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        if ('TESTRUN' in os.environ) and (
                not "SMOKE" in os.environ['TESTRUN']):
            assert check_file_exists(
                'TNS_App/platforms/ios',
                'platform_ios_current.txt')
        build(platform="ios", path="TNS_App")

    @unittest.skip(
        "This test is not valid, adding symlink platform from npm cache cause issues")
    def test_003_Platform_Add_iOS_Symlink(self):
        create_project(proj_name="TNS_App")
        output = platform_add(
            platform="ios",
            path="TNS_App",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        if ('TESTRUN' in os.environ) and (
                not "SMOKE" in os.environ['TESTRUN']):
            assert check_file_exists(
                'TNS_App/platforms/ios',
                'platform_ios_symlink.txt')

        # Verify Runtime is symlink
        output = run_aut("ls -la TNS_App/platforms/ios/")
        assert "NativeScript.framework ->" in output
        assert "package/framework/NativeScript.framework" in output

    def test_004_Platform_Add_iOS_Symlink_And_FrameworkPath(self):
        create_project(proj_name="TNS_App")
        output = platform_add(
            platform="ios",
            path="TNS_App",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        if ('TESTRUN' in os.environ) and (
                not "SMOKE" in os.environ['TESTRUN']):
            assert check_file_exists(
                'TNS_App/platforms/ios',
                'platform_ios_symlink.txt')

        # Verify Runtime is symlink
        output = run_aut("ls -la TNS_App/platforms/ios/")
        assert "internal ->" in output
        assert "package/framework/internal" in output

    def test_200_Platform_Add_iOS_FrameworkPath(self):
        create_project(proj_name="TNS_App")
        output = platform_add(
            platform="ios",
            framework_path=IOS_RUNTIME_PATH,
            path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        if ('TESTRUN' in os.environ) and (
                not "SMOKE" in os.environ['TESTRUN']):
            assert check_file_exists(
                'TNS_App/platforms/ios',
                'platform_ios_current.txt')

        # If project.xcworkspace is there Xcode project name is wrong
        assert not file_exists(
            "TNS_App/platforms/ios/TNSApp.xcodeproj/project.xcworkspace")

    def test_201_Platform_Remove_iOS(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_PATH)

        output = run_aut(TNSPATH + " platform remove ios --path TNS_App")
        assert "Platform ios successfully removed." in output

        assert not "error" in output
        assert is_empty('TNS_App/platforms')

        output = run_aut("cat TNS_App/package.json")
        assert not "tns-ios" in output

    def test_202_Platform_Remove_iOS_Symlink(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        output = run_aut(TNSPATH + " platform remove ios --path TNS_App")
        assert "Platform ios successfully removed." in output

        assert not "error" in output
        assert is_empty('TNS_App/platforms')

        output = run_aut("cat TNS_App/package.json")
        assert not "tns-ios" in output

    def test_300_Platform_Add_iOS_CustomVersion(self):
        create_project(proj_name="TNS_App")
        output = platform_add(platform="ios@1.4.0", path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        output = run_aut("cat TNS_App/package.json")
        assert "\"version\": \"1.4.0\"" in output

        if ('TESTRUN' in os.environ) and (
                not "SMOKE" in os.environ['TESTRUN']):
            assert check_file_exists(
                'TNS_App/platforms/ios',
                'platform_ios_1.4.0.txt')
        build(platform="ios", path="TNS_App")

    @unittest.skip(
        "Skip until fixed: https://github.com/NativeScript/nativescript-cli/issues/772")
    def test_301_Platform_Update_iOS(self):
        create_project(proj_name="TNS_App")
        output = platform_add(platform="ios@1.2.2", path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        output = run_aut("cat TNS_App/package.json")
        assert "\"version\": \"1.2.2\"" in output

        command = TNSPATH + " platform update ios@1.3.0 --path TNS_App < enter_key.txt"
        run_aut("echo " + command)
        os.system(command)

        output = run_aut("cat TNS_App/package.json")
        assert "\"version\": \"1.3.0\"" in output

        if ('TESTRUN' in os.environ) and (
                not "SMOKE" in os.environ['TESTRUN']):
            assert check_file_exists(
                'TNS_App/platforms/ios',
                'platform_ios_1.3.0.txt')
        build(platform="ios", path="TNS_App")

    @unittest.skip("This test fails on the build machine because it needs more time to update ios@1.1.0. Try to execute update command again with run_aut or add time.sleep(x).")
    def test_302_Platform_Downgrade_iOS_ToOlderVersion(self):
        create_project_add_platform(proj_name="TNS_App", platform="ios@1.2.0")
        output = run_aut("cat TNS_App/package.json")
        assert "\"version\": \"1.2.0\"" in output

        command = TNSPATH + " platform update ios@1.1.0 --path TNS_App < enter_key.txt"
        run_aut("echo " + command)
        os.system(command)

        output = run_aut("cat TNS_App/package.json")
        assert "\"version\": \"1.1.0\"" in output
        build(platform="ios", path="TNS_App")

    @unittest.skip(
        "Execute when platform update command starts respecting --frameworkPath: https://github.com/NativeScript/nativescript-cli/issues/743")
    def test_303_Platform_Update_iOS_ToLatestVersion(self):
        create_project_add_platform(proj_name="TNS_App", platform="ios@1.0.0")
        output = run_aut("cat TNS_App/package.json")
        assert "\"version\": \"1.0.0\"" in output

        command = TNSPATH + \
            " platform update ios --frameworkPath {0} --path TNS_App".format(
                IOS_RUNTIME_PATH)
        output = run_aut(command)
        assert "We need to override xcodeproj file. The old one will be saved at" in output

        # output = run_aut("echo '' | " + TNSPATH + " platform update")
        assert "Successfully updated to version  1.2.0" in output
        build(platform="ios", path="TNS_App")

    @unittest.skip(
        "Skip until fixed: https://github.com/NativeScript/nativescript-cli/issues/772")
    def test_304_Platform_Downgrade_iOS_FromLatestVersion(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_PATH)

        output = run_aut("cat TNS_App/package.json")
        assert "\"version\": \"1." in output

        command = TNSPATH + " platform update ios@1.1.0 --path TNS_App < enter_key.txt"
        run_aut("echo " + command)
        os.system(command)

        output = run_aut("cat TNS_App/package.json")
        assert "\"version\": \"1.1.0\"" in output
        build(platform="ios", path="TNS_App")

    def test_310_Platform_Add_iOS_CustomExperimentalVersion(self):
        create_project(proj_name="TNS_App")
        output = platform_add(platform="ios@0.9.2-exp-ios-8.2", path="TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created" in output

        output = run_aut("cat TNS_App/package.json")
        assert "\"version\": \"0.9.2-exp-ios-8.2\"" in output

    def test_320_Platform_Add_iOS_CustomBundleId(self):
        # Create project with different appId
        create_project(proj_name="TNS_App", app_id="org.nativescript.MyApp")
        output = run_aut("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.MyApp\"" in output

        # Add iOS platform
        output = platform_add(
            platform="ios",
            path="TNS_App",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        assert "Project successfully created" in output

        # Verify plist file
        output = run_aut("cat TNS_App/platforms/ios/TNSApp/TNSApp-Info.plist")
        assert "org.nativescript.MyApp" in output

    def test_330_Platform_Update_iOS_PlatformNotAdded(self):
        create_project(proj_name="TNS_App")
        output = run_aut(TNSPATH + " platform update ios --path TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert not is_empty("TNS_App/platforms/ios/internal/metadata-generator")

    def test_400_Platform_Add_AlreadyExistingPlatform(self):
        self.test_004_Platform_Add_iOS_Symlink_And_FrameworkPath()

        output = run_aut(TNSPATH + " platform add ios --path TNS_App")
        assert "Platform ios already added" in output
        assert "Usage" in output
