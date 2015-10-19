import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT, IsRunningProcess
from helpers._tns_lib import CreateProject, CreateProjectAndAddPlatform, \
    iosRuntimeSymlinkPath, tnsPath


class Emulate_OSX(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        
    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_AppNoPlatform');
    
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        CleanupFolder('./TNS_App');
    
    def test_001_Emulate_ListDevices(self):
        output = runAUT(tnsPath + " emulate ios --availableDevices --path TNS_App --justlaunch")
        assert ("iPhone-6" in output) 
        
    def test_002_Emulate_iOS(self):
        output = runAUT(tnsPath + " emulate ios --device iPhone-6 --path TNS_App --justlaunch")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Starting iOS Simulator" in output) 
        
        # Simulator can not be started without active UI 
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']): 
            assert ("Session started without errors" in output) 
            assert IsRunningProcess("Simulator")
        
    def test_003_Emulate_iOS_Release(self):
        output = runAUT(tnsPath + " emulate ios --device iPhone-6 --path TNS_App --release --justlaunch")
        assert ("Project successfully prepared" in output) 
        assert ("CONFIGURATION Release" in output)
        assert ("Project successfully built" in output)   
        assert ("Starting iOS Simulator" in output) 
        
        # Simulator can not be started without active UI 
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']): 
            assert ("Session started without errors" in output) 
            assert IsRunningProcess("Simulator")

    def test_210_Emulate_iOS_PlatformNotAdded(self):
        CreateProject(projName="TNS_AppNoPlatform")  
        output = runAUT(tnsPath + " emulate ios --device iPhone-6 --path TNS_AppNoPlatform --justlaunch")
        assert ("Copying template files..." in output)
        assert ("Project successfully created." in output)
        assert ("Project successfully prepared" in output)
        assert ("Project successfully built" in output)
        assert ("Starting iOS Simulator" in output)

        # Simulator can not be started without active UI
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']): 
            assert ("Session started without errors" in output)
            assert IsRunningProcess("Simulator")

    def test_400_Emulate_InvalidDevice(self):
        output = runAUT(tnsPath + " emulate ios --device invalidDevice --path TNS_App --justlaunch")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Invalid device identifier invalidDevice. Valid device identifiers are" in output)  