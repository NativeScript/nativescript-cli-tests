import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT, IsRunningProcess
from helpers._tns_lib import CreateProject, CreateProjectAndAddPlatform, \
    iosRuntimeSymlinkPath, tnsPath
from helpers.device import GivenRealDeviceRunning


class Run_OSX(unittest.TestCase):
 
    @classmethod
    def setUpClass(cls):
        
        GivenRealDeviceRunning(platform="ios") 
                
        CleanupFolder('./TNS_App')
        CleanupFolder('./TNSAppNoPlatform')
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True) 

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        CleanupFolder('./TNS_App')
        CleanupFolder('./TNSAppNoPlatform')

    
    def test_001_Run_iOS(self):
        output = runAUT(tnsPath + " run ios --path TNS_App --justlaunch")
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Debug" in output)
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device" in output)  
        #TODO: Get device id and verify files are deployed and process is running on this device 
    
    def test_002_Run_iOS_ReleaseConfiguration(self):
        output = runAUT(tnsPath + " run ios --release --path TNS_App --justlaunch")
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Release" in output)
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device" in output)         
        #TODO: Get device id and verify files are deployed and process is running on this device
 
    def test_003_Run_iOS_Simulator(self):
        output = runAUT(tnsPath + " run ios --emulator --path TNS_App --justlaunch")
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Debug" in output)
        assert ("Project successfully built" in output)   
        assert ("Starting iOS Simulator" in output)  
        
        # Simulator can not be started without active UI 
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']): 
            assert ("Session started without errors" in output) 
            assert IsRunningProcess("Simulator")
            
        #TODO: Get device id and verify files are deployed and process is running on this device 

    def test_004_Run_iOS_ReleaseConfiguration_Simulator(self):
        output = runAUT(tnsPath + " run ios --emulator --release --path TNS_App --justlaunch")
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Release" in output)
        assert ("Project successfully built" in output)   
        assert ("Starting iOS Simulator" in output)  
        
        # Simulator can not be started without active UI 
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']): 
            assert ("Session started without errors" in output) 
            assert IsRunningProcess("Simulator") 
            
        #TODO: Get device id and verify files are deployed and process is running on this device 

    def test_005_Run_iOS_Default(self):
        output = runAUT(tnsPath + " run ios --path TNS_App", 60)
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Debug" in output)
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device" in output)  
        assert ("Mounting" in output)
        assert ("Successfully run application" in output)
                
    def test_200_Run_iOS_InsideProject(self):
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir,"TNS_App"))    
        output = runAUT(os.path.join("..", tnsPath) + " run ios --path TNS_App --justlaunch")
        os.chdir(currentDir);
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Debug" in output)
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device" in output)

    def test_300_Run_iOS_PlatformNotAdded(self):
        CreateProject(projName="TNSAppNoPlatform")
        output = runAUT(tnsPath + " run ios --path TNSAppNoPlatform --justlaunch")

        assert ("Project successfully created." in output)
        assert ("Project successfully prepared" in output)
        assert ("Project successfully built" in output)
        assert ("Successfully deployed on device" in output)