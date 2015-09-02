import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT, IsRunningProcess
from helpers._tns_lib import CreateProject, CreateProjectAndAddPlatform, \
    iosRuntimeSymlinkPath, tnsPath


class Emulate_OSX(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App')

    def tearDown(self):        
        pass

    def test_001_Emulate_ListDevices(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)  
        output = runAUT(tnsPath + " emulate ios --availableDevices --path TNS_App --justlaunch")
        assert ("iPhone-6" in output) 
        # TODO: Update verification after https://github.com/NativeScript/nativescript-cli/issues/289 is fixed
        
    def test_002_Emulate_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)  
        output = runAUT(tnsPath + " emulate ios --device iPhone-6 --path TNS_App --justlaunch")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Starting iOS Simulator" in output) 
        
        # Simulator can not be started without active UI 
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']): 
            assert ("Session started without errors" in output) 
            assert IsRunningProcess("Simulator")
        
    def test_003_Emulate_iOS_Release(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)  
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
        CreateProject(projName="TNS_App")  
        output = runAUT(tnsPath + " emulate ios --device iPhone-6 --path TNS_App --justlaunch")
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
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)  
        output = runAUT(tnsPath + " emulate ios --device invalidDevice --path TNS_App --justlaunch")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Invalid device identifier invalidDevice. Valid device identifiers are" in output)  