import unittest

from helpers._os_lib import CleanupFolder, CheckFilesExists, CheckOutput, runAUT,\
    FileExists
from helpers._tns_lib import tnsPath, Build, CreateProject, PlatformAdd, LibraryAdd

class Library_Linux(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS App');
        CleanupFolder('./TNS_App');
        CleanupFolder('./folder');
        CleanupFolder('./template');

    def tearDown(self):        
        pass

    # Copying jar libraries log to be added
    def test_001_Library_Add_Android_JarLib(self):
        CreateProject(projName="TNS_App") 
        PlatformAdd(platform="android", path="TNS_App")
 
        LibraryAdd(platform="android", libPath="QA-TestApps/android-external-lib", path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_add_JarLib_1.1.0.txt"))
 
        Build(platform="android", path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_build_JarLib_1.1.0.txt"))

    def test_201_Library_Add_Android_ProjLib(self):
        CreateProject(projName="TNS_App", copyFrom="QA-TestApps/android-external-lib/external-lib") 
        PlatformAdd(platform="android", path="TNS_App")

        LibraryAdd(platform="android", libPath="QA-TestApps/android-external-lib/AndroidAppProject", path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_add_ProjLib_1.1.0.txt"))
 
        Build(platform="android", path="TNS_App")
        assert (CheckFilesExists("TNS_App", "library_build_ProjLib_1.1.0.txt"))

    #TODO: Implement this test.
    @unittest.skip("Not implemented.")  
    def test_202_Library_Add_Android_JarLibs(self):
        pass

    #TODO: Implement this test.
    @unittest.skip("Not implemented.")  
    def test_203_Library_Add_Android_SharedLibraries(self):
        pass

    def test_301_Library(self):
        output = runAUT(tnsPath + " library")
        assert CheckOutput(output, 'library_help_output.txt')

    def test_402_Library_Add_Platform_None(self):
        CreateProject(projName="TNS_App") 
        output = runAUT(tnsPath + " library add android QA-TestApps/ --path TNS_App")

        assert ("The platform android is not added to this project. Please use 'tns platform add <platform>'" in output)
        assert not FileExists("TNS_App/lib/Android/java-project.jar")