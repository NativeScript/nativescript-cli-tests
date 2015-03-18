import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import tnsPath, CreateProject, Prepare, \
    CreateProjectAndAddPlatform, iosRuntimeSymlinkPath


class Build_OSX(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        runAUT("sudo find /var/folders/ -name '*TNS_App-*' -exec rm -rf {} \;") # Delete precompiled headers
        CleanupFolder('./TNS_App')
        
    def tearDown(self):        
        pass

    def test_001_Build_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)     
        output = runAUT(tnsPath + " build ios --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("build/emulator/TNS_App.app" in output)  
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Project successfully built" in output)         
        assert FileExists("TNS_App/platforms/ios/build/emulator/TNS_App.app")
            
    def test_002_Build_iOS_Release(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)     
        output = runAUT(tnsPath + " build ios --path TNS_App --release")
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Release" in output)
        assert ("build/emulator/TNS_App.app" in output)  
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Project successfully built" in output)         
        assert FileExists("TNS_App/platforms/ios/build/emulator/TNS_App.app")

    def test_003_Build_iOS_ForDevice(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)     
        output = runAUT(tnsPath + " build ios --path TNS_App --forDevice")
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Debug" in output)
        assert ("CodeSign" in output)
        assert ("build/device/TNS_App.app" in output)  
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Project successfully built" in output)         
        assert FileExists("TNS_App/platforms/ios/build/device/TNS_App.ipa")
        
    def test_004_Build_iOS_Release_ForDevice(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)     
        output = runAUT(tnsPath + " build ios --path TNS_App --forDevice --release")
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Release" in output)
        assert ("CodeSign" in output)
        assert ("build/device/TNS_App.app" in output)  
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Project successfully built" in output)         
        assert FileExists("TNS_App/platforms/ios/build/device/TNS_App.ipa")
        
        # Verify ipa has both armv7 and arm64 archs
        output = runAUT("mv TNS_App/platforms/ios/build/device/TNS_App.ipa TNS_App-ipa.tgz")    
        output = runAUT("tar -xvf TNS_App-ipa.tgz")     
        output = runAUT("lipo -info Payload/TNS_App.app/TNS_App")
        assert ("armv7" in output)
        assert ("arm64" in output)       

    def test_200_Build_iOS_None_SymlinkProject(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath)     
        output = runAUT(tnsPath + " build ios --path TNS_App --forDevice --release")
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Release" in output)
        assert ("CodeSign" in output)
        assert ("build/device/TNS_App.app" in output)  
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Project successfully built" in output)         
        assert FileExists("TNS_App/platforms/ios/build/device/TNS_App.ipa")  

    def test_201_Build_iOS_InsideProject(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)  
        
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))    
        output = runAUT(os.path.join("..", tnsPath) + " build ios --path TNS_App")
        os.chdir(currentDir);

        assert ("Project successfully prepared" in output) 
        assert ("build/emulator/TNS_App.app" in output)  
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Project successfully built" in output)         
        assert FileExists("TNS_App/platforms/ios/build/emulator/TNS_App.app")

    def test_202_Build_iOS_WithPrepare(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)     
        Prepare(path="TNS_App", platform="ios") 
        
        output = runAUT(tnsPath + " build ios --path TNS_App")
        
        # Even if project is already prepared build will prepare it again
        assert ("Project successfully prepared" in output) 
        assert ("build/emulator/TNS_App.app" in output)  
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Project successfully built" in output)         
        assert FileExists("TNS_App/platforms/ios/build/emulator/TNS_App.app")
        
        # Verify Xcode project name is not empty
        command = "cat TNS_App/platforms/ios/TNS_App.xcodeproj/project.xcworkspace/contents.xcworkspacedata"
        output = runAUT(command)     
        assert not ("__PROJECT_NAME__.xcodeproj" in output)
                               
    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/277")             
    def test_400_Build_iOS_WhenPlatformIsNotAdded(self):
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " build ios --path TNS_App")
        # TODO: Verify after issue is fixed
        assert not ("error" in output)
        
    def test_401_Build_iOS_WithWrongParam(self):
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " build iOS --debug --path TNS_App")
        assert ("The option 'debug' is not supported." in output)
        assert not ("error" in output)