import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import CreateProjectAndAddPlatform, \
    tnsPath, androidKeyStorePath, androidKeyStorePassword, \
    androidKeyStoreAlias, androidKeyStoreAliasPassword, CreateProject, \
    androidRuntimePath
from helpers.device import GivenRunningEmulator, GivenRealDeviceRunning


class Run_Linux(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App')
        GivenRunningEmulator()
        GivenRealDeviceRunning(platform="android") 
        
    def tearDown(self):        
        pass

    def test_010_Run_Android(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " run android --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device with identifier" in output)  
        #TODO: Get device id and verify files are deployed and process is running on this device 
        
    def test_011_Run_Android_InsideProject(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)     
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))    
        output = runAUT(os.path.join("..", tnsPath) + " run android --path TNS_App")
        os.chdir(currentDir);
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device with identifier" in output)  
        
    def test_012_Run_Android_ReleaseConfiguration(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " run android --keyStorePath " + androidKeyStorePath + 
                        " --keyStorePassword " + androidKeyStorePassword + 
                        " --keyStoreAlias " + androidKeyStoreAlias + 
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword + 
                        " --release --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device with identifier" in output)         
        #TODO: Get device id and verify files are deployed and process is running on this device
 
    def test_013_Run_Android_DeviceId(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " run android --device emulator-5554 --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device with identifier 'emulator-5554'" in output)  
        #TODO: Get device id and verify files are deployed and process is running on this device 
                       
    def test_400_Run_MissingPlatform(self):
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " run android --path TNS_App")
        assert ("The platform android is not added to this project" in output) 
        
    def test_401_Run_InvalidPlatform(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " run invalidPlatform --path TNS_App")
        assert ("Invalid platform invalidplatform. Valid platforms are ios or android." in output) 
        
    def test_402_Run_InvalidDevice(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
        output = runAUT(tnsPath + " run android --device invalidDeviceId --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Cannot resolve the specified connected device by the provided index or identifier" in output)
        assert ("To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'" in output)