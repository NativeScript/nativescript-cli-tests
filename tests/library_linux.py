import unittest

from helpers._os_lib import CleanupFolder, CheckFilesExists, CheckOutput, runAUT, \
    FileExists, FolderExists
from helpers._tns_lib import androidRuntimePath, tnsPath, \
    Build, CreateProject, PlatformAdd, LibraryAdd

class Library_Linux(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App');

    def tearDown(self):
        pass

    def test_001_Library_Add_Android_JarLib(self):
        CreateProject(projName="TNS_App")
        PlatformAdd(platform="android", frameworkPath=androidRuntimePath, path="TNS_App")
 
        LibraryAdd(platform="android", libPath="QA-TestApps/external-lib", path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_add_JarLib_1.1.0.txt"))
 
        Build(platform="android", path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_build_JarLib_1.1.0.txt"))

    def test_002_Library_Add_Android_ProjLib(self):
        CreateProject(projName="TNS_App", copyFrom="QA-TestApps/external-lib/external-lib-android")
        PlatformAdd(platform="android", frameworkPath=androidRuntimePath, path="TNS_App")

        LibraryAdd(platform="android", libPath="QA-TestApps/external-lib/AndroidAppProject", path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_add_ProjLib_1.1.0.txt"))

        output = runAUT("cat TNS_App/lib/Android/AndroidAppProject/project.properties")
        assert ("target=android-22" in output)
        assert ("android.library=true" in output)

        Build(platform="android", path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_build_ProjLib_1.1.0.txt"))

    #TODO: Implement this test.
    @unittest.skip("Not implemented.")  
    def test_201_Library_Add_Android_JarLibs(self):
        pass

    #TODO: Implement this test.
    @unittest.skip("Not implemented.")  
    def test_202_Library_Add_Android_SharedLibraries(self):
        pass

    def test_301_Library(self):
        output = runAUT(tnsPath + " library")
        assert CheckOutput(output, 'library_help_output.txt')

    def test_401_Library_Add_Android_NoLib(self):
        CreateProject(projName="TNS_App", copyFrom="QA-TestApps/external-lib/external-lib-android")
        PlatformAdd(platform="android", frameworkPath=androidRuntimePath, path="TNS_App")
        output = LibraryAdd(platform="android", libPath="QA-TestApps/external-lib/external-lib-android", path="TNS_App", assertSuccess=False)
        assert ("Invalid library path" in output)
        assert not FolderExists("TNS_App/lib/Android")

    def test_402_Library_Add_NoPlatform(self):
        CreateProject(projName="TNS_App") 
        output = runAUT(tnsPath + " library add android QA-TestApps/ --path TNS_App")

        assert ("The platform android is not added to this project. Please use 'tns platform add <platform>'" in output)
        assert not FileExists("TNS_App/lib/Android/java-project.jar")
