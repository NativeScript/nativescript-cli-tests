import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import CreateProjectAndAddPlatform, iosRuntimeSymlinkPath, tnsPath
from helpers.device import GivenRealDeviceRunning


class Deploy_OSX(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App')
        GivenRealDeviceRunning(platform="ios") 
        
    def tearDown(self):        
        pass

    def test_001_Deploy_iOS_Simulator(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)  
        output = runAUT(tnsPath + " deploy ios --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device with identifier" in output)  
        #TODO: Get device id and verify files are deployed and process is running on this device 

    def test_002_Deploy_iOS_Device(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)  
        output = runAUT(tnsPath + " deploy ios --path TNS_App")
        assert ("Project successfully prepared" in output) 
        assert ("Project successfully built" in output)   
        assert ("Successfully deployed on device with identifier" in output)  
        #TODO: Get device id and verify files are deployed and process is running on this device 