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

    def test_001_Prepare_Android(self): 
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert("Project successfully prepared" in output)
        
        # Verify app and tns_modules from application folder are processed and avalable in platform folder
        assert FileExists('TNS_App/platforms/android/assets/app/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/android/assets/app/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/android/assets/app/tns_modules/application/application.ios.js')
        
    def test_200_Prepare_Android_InsideProject(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)    
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))    
        output = runAUT(os.path.join("..", tnsPath) + " prepare android")
        os.chdir(currentDir);
        assert("Project successfully prepared" in output)    

        # Verify app and tns_modules from application folder are processed and avalable in platform folder
        assert FileExists('TNS_App/platforms/android/assets/app/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/android/assets/app/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/android/assets/app/tns_modules/application/application.ios.js')

    def test_201_Prepare_PlatformThatIsNotAdded(self):
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " prepare android --path TNS_App");
        assert("Copying template files..." in output)
        assert("Updated project.properties" in output)
        assert("Updated local.properties" in output)
        assert("Project successfully created." in output)
        assert("Project successfully prepared" in output)

    def test_300_Prepare_Android_RemoveOldFiles(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert("Project successfully prepared" in output)
        assert FileExists('TNS_App/platforms/android/assets/app/app.css')
        
        runAUT("mv TNS_App/app/app.css TNS_App/app/appNew.css")
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert("Project successfully prepared" in output)
        assert FileExists('TNS_App/platforms/android/assets/app/appNew.css')
        assert not FileExists('TNS_App/platforms/android/assets/app/app.css')

    def test_301_Prepare_Android_PlatformSpecificFiles(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert("Project successfully prepared" in output)
        assert FileExists('TNS_App/platforms/android/assets/app/app.css')
        
        runAUT("cp TNS_App/app/app.js TNS_App/app/app.ios.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/app.android.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/appios.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/appandroid.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/ios.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/android.js")
        runAUT("cp TNS_App/app/app.css TNS_App/app/app.ios.css")
        runAUT("cp TNS_App/app/app.css TNS_App/app/app.android.css")
        runAUT("mv TNS_App/app/app.js TNS_App/app/appNew.js")  
        runAUT("mv TNS_App/app/app.css TNS_App/app/appNew.css") 
             
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert("Project successfully prepared" in output)
        assert FileExists('TNS_App/platforms/android/assets/app/app.css')
        assert FileExists('TNS_App/platforms/android/assets/app/app.js')
        assert FileExists('TNS_App/platforms/android/assets/app/appandroid.js')   
        assert FileExists('TNS_App/platforms/android/assets/app/appios.js') 
        assert FileExists('TNS_App/platforms/android/assets/app/android.js')   
        assert FileExists('TNS_App/platforms/android/assets/app/ios.js')          
        assert not FileExists('TNS_App/platforms/android/assets/app/app.ios.css')
        assert not FileExists('TNS_App/platforms/android/assets/app/app.android.css')    
                            
    def test_400_Prepare_MissingPlatform(self):
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " prepare --path TNS_App");
        assert("You need to provide all the required parameters." in output)    
    
    def test_401_Prepare_InvalidPlatform(self):
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " prepare windows --path TNS_App");
        assert("Invalid platform windows. Valid platforms are ios or android." in output)    

    @unittest.skip("Moved to test_201_Prepare_PlatformThatIsNotAdded - this is no more a negative case due to https://github.com/NativeScript/nativescript-cli/issues/785")
    def test_402_Prepare_PlatformThatIsNotAdded(self):
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " prepare android --path TNS_App");
        assert("The platform android is not added to this project. Please use 'tns platform add <platform>'" in output)    