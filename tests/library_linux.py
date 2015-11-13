'''
Test for library command in context of Android
'''
import unittest

from helpers._os_lib import cleanup_folder, check_file_exists, check_output, run_aut, \
    file_exists, folder_exists
from helpers._tns_lib import ANDROID_RUNTIME_PATH, TNSPATH, \
    build, create_project, platform_add, library_add


# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class LibraryAndroid(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_library_add_android_jar_lib(self):
        create_project(proj_name="TNS_App")
        platform_add(
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH,
            path="TNS_App")

        library_add(
            platform="android",
            lib_path="testdata/projects/external-lib-android",
            path="TNS_App")
        assert check_file_exists("TNS_App", "library_add_JarLib_1.4.0.txt")

        build(platform="android", path="TNS_App")
        assert check_file_exists("TNS_App", "library_build_JarLib_master.txt")

    # TODO: Implement this test.
    @unittest.skip("Not implemented.")
    def test_201_library_add_android_Lib(self):
        pass

    def test_301_library(self):
        output = run_aut(TNSPATH + " library")
        assert check_output(output, 'library_help_output.txt')

    def test_400_library_add_android_eclipse_proj_lib(self):
        create_project(
            proj_name="TNS_App",
            copy_from="QA-TestApps/external-lib/external-lib-android")
        platform_add(
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH,
            path="TNS_App")

        output = library_add(
            platform="android",
            lib_path="QA-TestApps/external-lib/AndroidAppProject",
            path="TNS_App",
            assert_success=False)
        assert "Unable to add android library" in output
        assert "You can use `library add` command only with " + \
            "path to folder containing one or more .jar files." in output

    def test_401_library_add_android_no_lib(self):
        create_project(
            proj_name="TNS_App",
            copy_from="QA-TestApps/external-lib/external-lib-android")
        platform_add(
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH,
            path="TNS_App")
        output = library_add(
            platform="android",
            lib_path="QA-TestApps/external-lib/external-lib-android",
            path="TNS_App",
            assert_success=False)
        assert "Invalid library path" in output
        assert not folder_exists("TNS_App/lib/Android")

    def test_402_library_add_no_platform(self):
        create_project(proj_name="TNS_App")
        output = run_aut(
            TNSPATH +
            " library add android QA-TestApps/ --path TNS_App")

        assert "The platform android is not added to this project. " + \
            "Please use 'tns platform add <platform>'" in output
        assert not file_exists("TNS_App/lib/Android/java-project.jar")
