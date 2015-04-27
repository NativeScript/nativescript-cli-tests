import fileinput
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import CreateProject, tnsPath


class Create(unittest.TestCase):
    
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

    def test_001_CreateProject(self):        
        CreateProject(projName="TNS_App")        
        output = runAUT("cat TNS_App/.tnsproject")
        assert ("\"id\": \"org.nativescript.TNSApp\"" in output)
        
        # TODO: Uncomment this after TNS template on Github is OK
        #assert(CheckFilesExists(projName, 'template_javascript_files.txt'))
        
    def test_002_CreateProjectWithPath(self):
        CreateProject(projName="TNS_App", path='folder/subfolder/')
        output = runAUT("cat folder/subfolder/TNS_App/.tnsproject")
        assert ("\"id\": \"org.nativescript.TNSApp\"" in output)
        
        # TODO: Uncomment this after TNS template on Github is OK
        # assert(CheckFilesExists('folder/subfolder/' + projName, 'template_javascript_files.txt'))
        
    def test_003_CreateProjectWithAppId(self):
        CreateProject(projName = "TNS_App", appId="org.nativescript.MyApp")
        output = runAUT("cat TNS_App/.tnsproject")
        assert ("\"id\": \"org.nativescript.MyApp\"" in output)
        
    def test_004_CreateProjectWithCopyFrom(self):        
        # Create initial template project
        CreateProject(projName="template")
        
        # Modify some files in template project
        for line in fileinput.input("template/app/LICENSE", inplace = 1): 
            print line.replace("Copyright (c) 2015, Telerik AD", "Copyright (c) 2015, Telerik A D"),
            
        # Create new project based on first one
        CreateProject(projName="TNS_App", copyFrom="template/app") 
        
        # Verify new project corresponds to name of the new project
        output = runAUT("cat TNS_App/.tnsproject")
        assert ("\"id\": \"org.nativescript.TNSApp\"" in output)
        
        # Verify that content of the new project is based on first project 
        output = runAUT("cat TNS_App/app/LICENSE")
        assert not ("Copyright (c) 2015, Telerik AD" in output)     
        assert ("Copyright (c) 2015, Telerik A D" in output)        
 
    def test_005_CreateProjectWithSpaceInName(self):        
        CreateProject(projName="\"TNS App\"");        
        output = runAUT("cat \"TNS App/.tnsproject\"");
        assert ("\"id\": \"org.nativescript.TNSApp\"" in output)
              
    def test_400_CreateProjectWithCopyFromWrongPath(self):
        output = runAUT(tnsPath + " create TNS_App --copy-from invalidFolder")
        assert ("no such file or directory" in output)
        
    def test_401_CreateProjectInAlreadyExistingFolder(self):        
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " create TNS_App")
        assert ("Path already exists and is not empty" in output)
        
    def test_402_CreateProjectWithWrongCopyFromCommand(self):      
        # Create initial template project
        CreateProject(projName="template")
        
        output = runAUT(tnsPath + " create TNS_App -copy-from template")
        assert not ("successfully created" in output)
        assert ("To see command's options, use '$ tns help create'" in output)
    
    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/271")     
    def test_403_CreateProjectWithWrongCopyFromCommand(self):      
        # Create initial template project
        CreateProject(projName="template")
                
        output = runAUT(tnsPath + " create TNS_App --copyFrom template")
        assert ("To see command's options, use '$ nativescript help create'. To see all commands use '$ nativescript help'." in output)
        # TODO: Update assert after https://github.com/NativeScript/nativescript-cli/issues/262 is fixed