import unittest

from helpers._os_lib import CleanupFolder, CheckFilesExists, CheckOutput, runAUT, \
    FileExists, FolderExists
from helpers._tns_lib import androidRuntimePath, tnsPath, \
    Build, create_project, platform_add, LibraryAdd

# pylint: disable=R0201, C0111


class Library_Linux(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_Library_Add_Android_JarLib(self):
        create_project(proj_name="TNS_App")
        platform_add(
            platform="android",
            framework_path=androidRuntimePath,
            path="TNS_App")

        LibraryAdd(
            platform="android",
            libPath="QA-TestApps/external-lib",
            path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_add_JarLib_1.4.0.txt"))

        Build(platform="android", path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_build_JarLib_master.txt"))

    # TODO: Implement this test.
    @unittest.skip("Not implemented.")
    def test_201_Library_Add_Android_Lib(self):
        pass

    def test_301_Library(self):
        output = runAUT(tnsPath + " library")
        assert CheckOutput(output, 'library_help_output.txt')

    def test_400_Library_Add_Android_EclipseProjLib(self):
        create_project(
            proj_name="TNS_App",
            copy_from="QA-TestApps/external-lib/external-lib-android")
        platform_add(
            platform="android",
            framework_path=androidRuntimePath,
            path="TNS_App")

        output = LibraryAdd(
            platform="android",
            libPath="QA-TestApps/external-lib/AndroidAppProject",
            path="TNS_App",
            assertSuccess=False)
        assert "Unable to add android library" in output
        assert "You can use `library add` command only with path to folder containing one or more .jar files." in output

    def test_401_Library_Add_Android_NoLib(self):
        create_project(
            proj_name="TNS_App",
            copy_from="QA-TestApps/external-lib/external-lib-android")
        platform_add(
            platform="android",
            framework_path=androidRuntimePath,
            path="TNS_App")
        output = LibraryAdd(
            platform="android",
            libPath="QA-TestApps/external-lib/external-lib-android",
            path="TNS_App",
            assertSuccess=False)
        assert "Invalid library path" in output
        assert not FolderExists("TNS_App/lib/Android")

    def test_402_Library_Add_NoPlatform(self):
        create_project(proj_name="TNS_App")
        output = runAUT(
            tnsPath +
            " library add android QA-TestApps/ --path TNS_App")

        assert "The platform android is not added to this project. Please use 'tns platform add <platform>'" in output
        assert not FileExists("TNS_App/lib/Android/java-project.jar")
