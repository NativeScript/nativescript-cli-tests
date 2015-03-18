import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import CreateProjectAndAddPlatform, androidRuntimePath, \
    tnsPath, androidKeyStorePath, androidKeyStorePassword, androidKeyStoreAlias, \
    androidKeyStoreAliasPassword, CreateProject
from helpers.device import StopEmulators, GivenRunningEmulator


class Emulate_Linux(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App')
        GivenRunningEmulator()
        
    def tearDown(self):        
        pass

    def test_001_Emulate_Android_InRunningEmulator(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " emulate android --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output) 
        assert ("installing" in output) 
        assert ("running" in output)   
        assert not ("Starting Android emulator with image" in output)
        #TODO: Get device id and verify files are deployed and process is running on this device 
        
    def test_002_Emulate_Android_ReleaseConfiguration(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " emulate android --keyStorePath " + androidKeyStorePath + 
                        " --keyStorePassword " + androidKeyStorePassword + 
                        " --keyStoreAlias " + androidKeyStoreAlias + 
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword + 
                        " --release --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("installing" in output) 
        assert ("running" in output)          
        assert not ("Starting Android emulator with image" in output)
        #TODO: Get device id and verify files are deployed and process is running on this device
 
    #TODO: Implement this test 
    @unittest.skip("Not implemented.")     
    def test_014_Emulate_Android_Genymotion(self):
        pass

    def test_200_Emulate_Android_InsideProject_InRunningEmulator(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)     
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))    
        output = runAUT(os.path.join("..", tnsPath) + " emulate android --path TNS_App")
        os.chdir(currentDir);
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("installing" in output) 
        assert ("running" in output)   
        #TODO: Get device id and verify files are deployed and process is running on this device
        
    def test_201_Emulate_Android_AvdName(self):
        StopEmulators();
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " emulate android --avd Api19 --path TNS_App")
        assert ("Starting Android emulator with image Api19" in output)
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("installing" in output) 
        assert ("running" in output)   
        #TODO: Get device id and verify files are deployed and process is running on this device 
                                       
    def test_400_Emulate_MissingPlatform(self):
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " emulate android --path TNS_App")
        assert ("The platform android is not added to this project" in output) 
        
    def test_401_Emulate_InvalidPlatform(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " emulate invalidPlatform --path TNS_App")
        assert ("The input is not valid sub-command for 'emulate' command" in output) 
        assert ("Usage:" in output) 
 
    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/289")    
    def test_402_Emulate_InvalidAvd(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " emulate android --avd invalidDeviceId --path TNS_App")
        # TODO: Modify assert when issue is fixed
        assert ("'invalidPlatform' is not valid sub-command for 'emulate' command" in output) 
        assert ("Usage:" in output) 