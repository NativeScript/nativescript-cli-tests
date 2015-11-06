import unittest

from helpers._os_lib import cleanup_folder, check_file_exists, check_output, run_aut, \
    file_exists, folder_exists
from helpers._tns_lib import ANDROID_RUNTIME_PATH, TNSPATH, \
    build, create_project, platform_add, library_add

# pylint: disable=R0201, C0111


class Library_Linux(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_Library_Add_Android_JarLib(self):
        create_project(proj_name="TNS_App")
        platform_add(
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH,
            path="TNS_App")

        library_add(
            platform="android",
            lib_path="QA-TestApps/external-lib",
            path="TNS_App")
        assert (check_file_exists("TNS_App", "library_add_JarLib_1.4.0.txt"))

        build(platform="android", path="TNS_App")
        assert (check_file_exists("TNS_App", "library_build_JarLib_master.txt"))

    # TODO: Implement this test.
    @unittest.skip("Not implemented.")
    def test_201_Library_Add_Android_Lib(self):
        pass

    def test_301_Library(self):
        output = run_aut(TNSPATH + " library")
        assert check_output(output, 'library_help_output.txt')

    def test_400_Library_Add_Android_EclipseProjLib(self):
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
        assert "You can use `library add` command only with path to folder containing one or more .jar files." in output

    def test_401_Library_Add_Android_NoLib(self):
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

    def test_402_Library_Add_NoPlatform(self):
        create_project(proj_name="TNS_App")
        output = run_aut(
            TNSPATH +
            " library add android QA-TestApps/ --path TNS_App")

        assert "The platform android is not added to this project. Please use 'tns platform add <platform>'" in output
        assert not file_exists("TNS_App/lib/Android/java-project.jar")
