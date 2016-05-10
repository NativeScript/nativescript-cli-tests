"""
Tests for building projects with the Android platform
"""
import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_ALIAS_PASS, CURRENT_OS, \
    OSType, ANDROID_RUNTIME_SYMLINK_PATH, TEST_RUN_HOME
from core.tns.tns import Tns


class BuildAndroid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        File.remove("TNSApp-debug.apk")
        File.remove("TNSApp-release.apk")

        Folder.cleanup('./tns-app')
        Folder.cleanup('./TNS App')
        Folder.cleanup('./TNS_App')
        Folder.cleanup('./TNS_AppSymlink')
        Tns.create_app_platform_add(app_name="TNS_App", platform="android", framework_path=ANDROID_RUNTIME_PATH)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNSAppNoPlatform')
        Folder.cleanup('./TNS_App/platforms/android/build/outputs')
        Folder.cleanup('./TNS_App/platforms/android/build/intermediates/exploded-aar')
        # TODO: Do not delete exploder-aar after https://github.com/NativeScript/android-runtime/issues/339 is fixed

    def tearDown(self):
        Folder.cleanup('./TNSAppNoPlatform')
        Folder.cleanup('./TNS_App/platforms/android/build/outputs')
        Folder.cleanup('./TNS_App/platforms/android/build/intermediates/exploded-aar')
        # TODO: Do not delete exploder-aar after https://github.com/NativeScript/android-runtime/issues/339 is fixed

    @classmethod
    def tearDownClass(cls):
        File.remove("TNSApp-debug.apk")
        File.remove("TNSApp-release.apk")

        Folder.cleanup('./tns-app')
        Folder.cleanup('./TNS App')
        Folder.cleanup('./TNS_AppSymlink')

    def test_001_build_android(self):
        output = run(TNS_PATH + " build android --path TNS_App")
        assert "Project successfully prepared" in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

        assert "ERROR" not in output
        assert "FAILURE" not in output

        assert File.exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_002_build_android_release(self):
        output = run(TNS_PATH + " build android --keyStorePath " + ANDROID_KEYSTORE_PATH +
                     " --keyStorePassword " + ANDROID_KEYSTORE_PASS +
                     " --keyStoreAlias " + ANDROID_KEYSTORE_ALIAS +
                     " --keyStoreAliasPassword " + ANDROID_KEYSTORE_ALIAS_PASS +
                     " --release --path TNS_App")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Ignore because of https://github.com/NativeScript/nativescript-cli/issues/282")
    def test_100_build_android_symlink(self):
        Tns.create_app(app_name="TNS_AppSymlink")
        output = Tns.platform_add(platform="android", path="TNS_AppSymlink",
                                  framework_path=ANDROID_RUNTIME_SYMLINK_PATH, symlink=True)
        assert "Project successfully created" in output
        output = run(TNS_PATH + " build android --path TNS_AppSymlink")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

        # Verify build does not modify original manifest
        output = run("cat " + ANDROID_RUNTIME_SYMLINK_PATH +
                     "/framework/src/main/AndroidManifest.xml")
        assert "__PACKAGE__" in output, \
            "Build modify original AndroidManifest.xml, this is a problem!"
        assert "__APILEVEL__" in output, \
            "Build modify original AndroidManifest.xml, this is a problem!"

    def test_200_build_android_inside_project_folder(self):
        Folder.navigate_to("TNS_App")
        output = run(os.path.join("..", TNS_PATH) +
                     " build android --path TNS_App")
        Folder.navigate_to(TEST_RUN_HOME, relative_from__current_folder=False)
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_201_build_android_with_additional_prepare(self):

        Tns.prepare(path="TNS_App", platform="android")
        output = run(TNS_PATH + " build android --path TNS_App")

        # Even if project is already prepared build will prepare it again
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_202_build_android_platform_not_added(self):
        Tns.create_app(app_name="TNSAppNoPlatform")
        output = run(TNS_PATH + " build android --path TNSAppNoPlatform --log trace")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

        assert "ERROR" not in output
        assert "FAILURE" not in output
        assert File.exists("TNSAppNoPlatform/platforms/android"
                           "/build/outputs/apk/TNSAppNoPlatform-debug.apk")

    def test_203_build_android_platform_when_platform_folder_is_empty(self):
        Tns.create_app(app_name="TNSAppNoPlatform")
        Folder.cleanup('./TNSAppNoPlatform/platforms')
        output = run(TNS_PATH + " build android --path TNSAppNoPlatform  --log trace")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

        assert "ERROR" not in output
        assert "FAILURE" not in output
        assert File.exists("TNSAppNoPlatform/platforms/android"
                           "/build/outputs/apk/TNSAppNoPlatform-debug.apk")

    def test_300_build_android_with_additional_styles_xml(self):

        # This is test for issue 644

        run("mkdir -p TestApp/app/App_Resources/Android/values")
        run("cp data/data/styles.xml TestApp/app/App_Resources/Android/values")
        output = run(TNS_PATH + " build android --path TNS_App")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert File.exists(
                "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_301_build_project_with_dash(self):
        Tns.create_app_platform_add(app_name="tns-app",
                                    platform="android", framework_path=ANDROID_RUNTIME_PATH)

        # Verify project builds
        output = run(TNS_PATH + " build android --path tns-app")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert File.exists(
                "tns-app/platforms/android/build/outputs/apk/tnsapp-debug.apk")

        # Verify project id
        output = run("cat tns-app/package.json")
        assert "org.nativescript.tnsapp" in output

        # Verify AndroidManifest.xml
        output = run(
                "cat tns-app/platforms/android/src/main/AndroidManifest.xml")
        assert "org.nativescript.tnsapp" in output

    def test_302_build_project_with_space(self):
        Tns.create_app_platform_add(app_name="\"TNS App\"",
                                    platform="android", framework_path=ANDROID_RUNTIME_PATH)

        # Verify project build
        output = run(TNS_PATH + " build android --path \"TNS App\"")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert File.exists(
                "TNS App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

        if CURRENT_OS == OSType.WINDOWS:
            # Verify project id
            output = run("cat \"TNS App/package.json\"")
            assert "org.nativescript.TNSApp" in output

            # Verify AndroidManifest.xml
            output = run(
                    "cat \"TNS App/platforms/android/src/main/AndroidManifest.xml\"")
            assert "org.nativescript.TNSApp" in output

        elif CURRENT_OS == OSType.OSX:
            # Verify project id
            output = run("cat TNS\\ App/package.json")
            assert "org.nativescript.TNSApp" in output

            # Verify AndroidManifest.xml
            output = run(
                    "cat TNS\\ App/platforms/android/src/main/AndroidManifest.xml")
            assert "org.nativescript.TNSApp" in output

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Skip on Windows, because tar is not available")
    def test_303_build_project_with_gz_file(self):
        run("tar -czf TNS_App/app/app.tar.gz TNS_App/app/app.js")
        assert File.exists("TNS_App/app/app.tar.gz")
        output = run(TNS_PATH + " build android --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

    def test_310_build_android_with_sdk22(self):
        output = run(TNS_PATH +
                     " build android --compileSdk 22 --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert "ERROR" not in output
        assert "FAILURE" not in output

        assert File.exists(
                "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_311_build_android_with_sdk23(self):

        output = run(
                TNS_PATH +
                " build android --compileSdk 23 --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert "ERROR" not in output
        assert "FAILURE" not in output

        assert File.exists(
                "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_312_build_android_with_sdk19(self):

        output = run(
                TNS_PATH +
                " build android --compileSdk 19 --path TNS_App --log trace")
        assert "Project successfully prepared" in output
        assert "BUILD FAILED" in output

    def test_313_build_android_with_sdk99(self):

        output = run(
                TNS_PATH +
                " build android --compileSdk 99 --path TNS_App")
        assert "You have specified '99' for compile sdk," \
               " but it is not installed on your system." in output

    def test_320_build_release_with_copyto_option(self):
        output = run(TNS_PATH + " build android --keyStorePath " + ANDROID_KEYSTORE_PATH +
                     " --keyStorePassword " + ANDROID_KEYSTORE_PASS +
                     " --keyStoreAlias " + ANDROID_KEYSTORE_ALIAS +
                     " --keyStoreAliasPassword " + ANDROID_KEYSTORE_ALIAS_PASS +
                     " --release --path TNS_App --copy-to ./")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        assert "Project successfully built" in output
        assert File.exists(
                "TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")
        assert File.exists("TNSApp-release.apk")

    def test_321_build_with_copyto_option(self):
        output = run(TNS_PATH + " build android --path TNS_App --copy-to ./")
        assert "Project successfully prepared" in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

        assert "ERROR" not in output
        assert "FAILURE" not in output

        assert File.exists(
                "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert File.exists("TNSApp-debug.apk")

    def test_400_build_with_no_platform(self):
        output = run(TNS_PATH + " build")
        assert "The input is not valid sub-command for 'build' command" in output
        assert "# build" in output

        if CURRENT_OS == OSType.OSX:
            assert "$ tns build <Platform>" in output
        else:
            assert "$ tns build android" in output

    def test_401_build_invalid_platform(self):
        output = run(TNS_PATH + " build invalidCommand")
        assert "The input is not valid sub-command for 'build' command" in output

    def test_402_build_no_path(self):
        output = run(TNS_PATH + " build android")
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_403_build_invalid_path(self):
        output = run(TNS_PATH + " build android --path invalidPath")
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_404_build_invalid_option(self):
        output = run(
                TNS_PATH +
                " build android --invalidOption --path TNS_App")
        assert "The option 'invalidOption' is not supported" in output

    @unittest.skipIf(CURRENT_OS == OSType.OSX)
    def test_405_build_ios_on_linux_machine(self):
        output = run(TNS_PATH + " build ios --path TNS_App")
        assert "Applications for platform ios can not be built on this OS" in output

    def test_406_build_release_without_key_options(self):
        output = run(TNS_PATH + " build android --release --path TNS_App")

        assert "When producing a release build, " \
               "you need to specify all --key-store-* options." in output
        assert "# build android" in output
        assert not File.exists(
                "TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")
