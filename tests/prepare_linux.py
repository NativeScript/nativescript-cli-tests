import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import CreateProject, tnsPath, androidRuntimePath, CreateProjectAndAddPlatform


class Prepare_Linux(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App');

    def tearDown(self):        
        pass

    def test_010_Prepare_Android(self): 
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert("Project successfully prepared" in output)
        
        # Verify app and tns_modules from application folder are processed and avalable in platform folder
        assert FileExists('TNS_App/platforms/android/assets/app/bootstrap.js')
        assert FileExists('TNS_App/platforms/android/assets/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/android/assets/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/android/assets/tns_modules/application/application.ios.js')
        
    def test_011_Prepare_Android_InsideProject(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)    
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))    
        output = runAUT(os.path.join("..", tnsPath) + " prepare android")
        os.chdir(currentDir);
        assert("Project successfully prepared" in output)    

        # Verify app and tns_modules from application folder are processed and avalable in platform folder
        assert FileExists('TNS_App/platforms/android/assets/app/bootstrap.js')
        assert FileExists('TNS_App/platforms/android/assets/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/android/assets/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/android/assets/tns_modules/application/application.ios.js')
                
    def test_400_Prepare_MissingPlatform(self):
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " prepare --path TNS_App");
        assert("You need to provide all the required parameters." in output)    
    
    def test_401_Prepare_InvalidPlatform(self):
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " prepare windows --path TNS_App");
        assert("Invalid platform windows. Valid platforms are ios or android." in output)    
    
    def test_402_Prepare_PlatformThatIsNotAdded(self):
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " prepare android --path TNS_App");
        assert("The platform android is not added to this project. Please use 'tns platform add <platform>'" in output)    