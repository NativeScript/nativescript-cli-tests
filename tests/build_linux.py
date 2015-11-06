'''
Tests for building projects with the Android platform
'''
import os
import platform
import unittest

from helpers._os_lib import cleanup_folder, remove, run_aut, file_exists
from helpers._tns_lib import tnsPath, create_project, create_project_add_platform, \
    androidRuntimePath, prepare, androidKeyStorePath, androidKeyStorePassword, \
    androidKeyStoreAlias, androidKeyStoreAliasPassword, platform_add, \
    androidRuntimeSymlinkPath

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class BuildAndroid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        remove("TNSApp-debug.apk")
        remove("TNSApp-release.apk")

        cleanup_folder('./tns-app')
        cleanup_folder('./TNS_App')
        cleanup_folder('./TNS_AppSymlink')
        create_project_add_platform(proj_name="TNS_App", \
                                    platform="android", framework_path=androidRuntimePath)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNSAppNoPlatform')
        cleanup_folder('./TNS_App/platforms/android/build/outputs')

    def tearDown(self):
        cleanup_folder('./TNSAppNoPlatform')
        cleanup_folder('./TNS_App/platforms/android/build/outputs')

    @classmethod
    def tearDownClass(cls):
        remove("TNSApp-debug.apk")
        remove("TNSApp-release.apk")

        cleanup_folder('./tns-app')
        cleanup_folder('./TNS_App')
        cleanup_folder('./TNS_AppSymlink')

    def test_001_build_android(self):
        output = run_aut(tnsPath + " build android --path TNS_App")
        assert "Project successfully prepared" in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

        assert not "ERROR" in output
        assert not "FAILURE" in output

        assert file_exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_002_build_android_release(self):
        output = run_aut(tnsPath + " build android --keyStorePath " + androidKeyStorePath +
                        " --keyStorePassword " + androidKeyStorePassword +
                        " --keyStoreAlias " + androidKeyStoreAlias +
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword +
                        " --release --path TNS_App")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")

    def test_100_build_android_symlink(self):
        if 'Windows' in platform.platform():
            print "Ignore because of https://github.com/NativeScript/nativescript-cli/issues/282"
        else:
            create_project(proj_name="TNS_AppSymlink")
            output = platform_add(platform="android", path="TNS_AppSymlink",
                                 framework_path=androidRuntimeSymlinkPath, symlink=True)
            assert "Project successfully created" in output
            output = run_aut(tnsPath + " build android --path TNS_AppSymlink")
            assert "Project successfully prepared" in output
            assert "BUILD SUCCESSFUL" in output
            assert "Project successfully built" in output

            # Verify build does not modify original manifest
            output = run_aut("cat " + androidRuntimeSymlinkPath +
                   "/framework/src/main/AndroidManifest.xml")
            assert "__PACKAGE__" in output, \
                "Build modify original AndroidManifest.xml, this is a problem!"
            assert "__APILEVEL__" in output, \
                "Build modify original AndroidManifest.xml, this is a problem!"

    def test_200_build_android_inside_project_folder(self):
        current_dir = os.getcwd();
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut(os.path.join("..", tnsPath) +
                        " build android --path TNS_App")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_201_build_android_with_additional_prepare(self):

        prepare(path="TNS_App", platform="android")
        output = run_aut(tnsPath + " build android --path TNS_App")

        # Even if project is already prepared build will prepare it again
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert file_exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_202_build_android_platform_not_added(self):
        create_project(proj_name="TNSAppNoPlatform")
        output = run_aut(tnsPath + " build android --path TNSAppNoPlatform --log trace")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

        assert not "ERROR" in output
        assert not "FAILURE" in output
        assert file_exists("TNSAppNoPlatform/platforms/android" \
                          "/build/outputs/apk/TNSAppNoPlatform-debug.apk")

    def test_203_build_android_platform_when_platform_folder_is_empty(self):
        create_project(proj_name="TNSAppNoPlatform")
        cleanup_folder('./TNSAppNoPlatform/platforms')
        output = run_aut(tnsPath + " build android --path TNSAppNoPlatform  --log trace")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

        assert not "ERROR" in output
        assert not "FAILURE" in output
        assert file_exists("TNSAppNoPlatform/platforms/android" \
                          "/build/outputs/apk/TNSAppNoPlatform-debug.apk")

    def test_300_build_android_with_additional_styles_xml(self):

        # This is test for issue 644

        run_aut("mkdir -p TestApp/app/App_Resources/Android/values")
        run_aut("cp testdata/data/styles.xml TestApp/app/App_Resources/Android/values")
        output = run_aut(tnsPath + " build android --path TNS_App")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert file_exists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_301_build_project_with_dash(self):
        create_project_add_platform(proj_name="tns-app",
                                    platform="android", framework_path=androidRuntimePath)

        # Verify project builds
        output = run_aut(tnsPath + " build android --path tns-app")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert file_exists(
            "tns-app/platforms/android/build/outputs/apk/tnsapp-debug.apk")

        # Verify project id
        output = run_aut("cat tns-app/package.json")
        assert "org.nativescript.tnsapp" in output

        # Verify AndroidManifest.xml
        output = run_aut(
            "cat tns-app/platforms/android/src/main/AndroidManifest.xml")
        assert "org.nativescript.tnsapp" in output

    def test_302_build_project_with_gz_file(self):
        # TODO: Find better way to skip tests on different OS
        # Skip on Windows, because tar is not available
        if 'Windows' not in platform.platform():
            run_aut("tar -czf TNS_App/app/app.tar.gz TNS_App/app/app.js")
            assert file_exists("TNS_App/app/app.tar.gz")

        output = run_aut(tnsPath + " build android --path TNS_App")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

    def test_310_build_android_with_sdk22(self):

        output = run_aut(
            tnsPath +
            " build android --compileSdk 22 --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output
        assert not "FAILURE" in output

        assert file_exists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_311_build_android_with_sdk23(self):

        output = run_aut(
            tnsPath +
            " build android --compileSdk 23 --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output
        assert not "FAILURE" in output

        assert file_exists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_312_build_android_with_sdk19(self):

        output = run_aut(
            tnsPath +
            " build android --compileSdk 19 --path TNS_App --log trace")
        assert "Project successfully prepared" in output
        assert "BUILD FAILED" in output

    def test_313_build_android_with_sdk99(self):

        output = run_aut(
            tnsPath +
            " build android --compileSdk 99 --path TNS_App")
        assert "Project successfully prepared" in output
        assert "You have specified '99' for compile sdk," \
            " but it is not installed on your system." in output

    def test_320_build_release_with_copyto_option(self):
        output = run_aut(tnsPath + " build android --keyStorePath " + androidKeyStorePath +
                        " --keyStorePassword " + androidKeyStorePassword +
                        " --keyStoreAlias " + androidKeyStoreAlias +
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword +
                        " --release --path TNS_App --copy-to ./")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        assert "Project successfully built" in output
        assert file_exists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")
        assert file_exists("TNSApp-release.apk")

    def test_321_build_with_copyto_option(self):
        output = run_aut(tnsPath + " build android --path TNS_App --copy-to ./")
        assert "Project successfully prepared" in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output

        assert not "ERROR" in output
        assert not "FAILURE" in output

        assert file_exists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert file_exists("TNSApp-debug.apk")

    def test_400_build_with_no_platform(self):
        output = run_aut(tnsPath + " build")
        assert "The input is not valid sub-command for 'build' command" in output
        assert "# build" in output

        if 'Darwin' in platform.platform():
            assert "$ tns build <Platform>" in output
        else:
            assert "$ tns build android" in output

    def test_401_build_invalid_platform(self):
        output = run_aut(tnsPath + " build invalidCommand")
        assert "The input is not valid sub-command for 'build' command" in output

    def test_402_build_no_path(self):
        output = run_aut(tnsPath + " build android")
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_403_build_invalid_path(self):
        output = run_aut(tnsPath + " build android --path invalidPath")
        assert "No project found at or above" in output
        assert "and neither was a --path specified." in output

    def test_404_build_invalid_option(self):
        output = run_aut(
            tnsPath +
            " build android --invalidOption --path TNS_App")
        assert "The option 'invalidOption' is not supported" in output

    def test_405_build_ios_on_linux_machine(self):
        output = run_aut(tnsPath + " build ios --path TNS_App")
        if 'Darwin' in platform.platform():
            pass
        else:
            assert "Applications for platform ios can not be built on this OS" in output

    def test_406_build_release_without_key_options(self):
        output = run_aut(tnsPath + " build android --release --path TNS_App")

        assert "When producing a release build, "\
            "you need to specify all --key-store-* options." in output
        assert "# build android" in output
        assert not file_exists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")
