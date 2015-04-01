from time import sleep
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import tnsPath, CreateProjectAndAddPlatform, \
    androidRuntimePath
from helpers.adb import StopApplication, WaitUntilAppIsRunning
from helpers.device import GetDeviceCount, GetPhysicalDeviceId, \
    GivenRealDeviceRunning, GivenRunningEmulator


class Device_Linux(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""
        
        CleanupFolder('./TNS_App')
        GivenRealDeviceRunning(platform="android")
        GivenRunningEmulator()
        
    def tearDown(self):        
        pass
    
    def test_001_Device_ListApplications_And_Run_Android(self):          
        deviceId = GetPhysicalDeviceId(platform="android");
        if (deviceId is not None): 
            
            # Deploy TNS_App on device
            CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
            output = runAUT(tnsPath + " deploy android --path TNS_App")
            assert ("Project successfully prepared" in output) 
            assert ("Project successfully built" in output)   
            assert ("Successfully deployed on device with identifier" in output)  
            assert (deviceId in output)  
            sleep(10)
            
            # Verify list-applications command list org.nativescript.TNSApp
            output = runAUT(tnsPath + " device list-applications --device " + deviceId)
            assert ("com.android." in output) 
            assert ("com.google." in output) 
            assert ("org.nativescript.TNSApp" in output)
            
            # Verify app is running    
            WaitUntilAppIsRunning(appId="org.nativescript.TNSApp", deviceId=deviceId, timeout = 60)
            
            # Kill the app
            StopApplication(appId="org.nativescript.TNSApp", deviceId=deviceId)
            
            # Start via run command and verify it is running
            runAUT(tnsPath + " device run org.nativescript.TNSApp --device " + deviceId)            
            
            # Verify app is running    
            WaitUntilAppIsRunning(appId="org.nativescript.TNSApp", deviceId=deviceId, timeout = 60)
            
        else:
            print "Prerequisites not met. This test requires at least one real android device."
            assert (False)             
 
    def test_002_Device_Log_Android(self): 
        if (GetDeviceCount(platform="android") > 1): 
            output = runAUT(tnsPath + " device log")
            assert ("More than one device found. Specify device explicitly." in output) 
        else:
            print "Prerequisites not met. This test requires at least two attached devices."
            assert (False)
                  
    def test_400_Device_InvalidPlatform(self):
        output = runAUT(tnsPath + " device windows")
        assert ("'windows' is not a valid device platform." in output) 
        assert ("Usage" in output) 
        
    def test_401_Device_Log_InvalidDeviceId(self):
        output = runAUT(tnsPath + " device log --device invalidDeviceId")
        assert ("Cannot resolve the specified connected device by the provided index or identifier." in output) 
        assert ("To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'." in output) 
        assert ("Usage" in output) 
    
    def test_402_Device_Run_InvalidDeviceId(self):
        output = runAUT(tnsPath + " device run  --device invalidDeviceId")
        assert ("Cannot resolve the specified connected device by the provided index or identifier." in output) 
        assert ("To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'." in output) 
        assert ("Usage" in output) 
    
    def test_403_Device_ListApplications_InvalidDeviceId(self):
        output = runAUT(tnsPath + " device list-applications --device invalidDeviceId")
        assert ("Cannot resolve the specified connected device by the provided index or identifier." in output) 
        assert ("To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'." in output) 
        assert ("Usage" in output) 