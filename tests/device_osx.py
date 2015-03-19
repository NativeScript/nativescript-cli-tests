from time import sleep
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import tnsPath, CreateProjectAndAddPlatform, androidRuntimePath, iosRuntimeSymlinkPath
from helpers.device import GivenRealDeviceRunning, GetPhysicalDeviceId

class Device_OSX(unittest.TestCase):
    
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
    
    def test_001_Device_Log_ListApplications_And_Run_Android(self):
                
        deviceId = GetPhysicalDeviceId(platform="android")
        if (deviceId is not None): 
            
            # Start DeviceLog 
            runAUT(tnsPath + " device log --device " + deviceId + " > deviceLog.txt &", None, False)
            
            # Deploy TNS_App on device
            CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)  
            output = runAUT(tnsPath + " deploy android --path TNS_App")
            assert ("Project successfully prepared" in output) 
            assert ("Project successfully built" in output)   
            assert ("Successfully deployed on device with identifier" in output)  
            assert (deviceId in output)
            sleep(10)
                        
            # Get list installed apps
            output = runAUT(tnsPath + " device list-applications --device " + deviceId)
            assert ("org.nativescript.TNSApp" in output)
            
            # Kill running app
            runAUT("adb -s " + deviceId + " shell pm clear org.nativescript.TNSApp")
            sleep(5)
            output = runAUT("adb -s " + deviceId + " shell ps | grep org.nativescript.TNSApp")
            assert not ("org.nativescript.TNSApp" in output)
                        
            # Start it via device command and verify app is running
            output = runAUT(tnsPath + " device run org.nativescript.TNSApp --device " + deviceId)            
            sleep(20)            
            output = runAUT("adb -s " + deviceId + " shell ps | grep org.nativescript.TNSApp")
            assert ("org.nativescript.TNSApp" in output)
            
            # Stop logging and print it
            runAUT("ps -A | grep \"device " + deviceId + "\" | awk '{print $1}' | xargs kill -9")
            runAUT("cat deviceLog.txt")
        else:
            print "Prerequisites not met. This test requires at least one real android device."
            assert (False)       

    @unittest.skip("Skipped because of https://github.com/NativeScript/nativescript-cli/issues/248")             
    def test_020_Device_Log_ListApplications_And_Run_iOS(self):          
        deviceId = GetPhysicalDeviceId(platform="ios")
        if (deviceId is not None): 
            
            # Start DeviceLog 
            runAUT(tnsPath + " device log --device " + deviceId + " > deviceLog.txt &", None, False)
            
            # Deploy TNS_App on device
            CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)     
            output = runAUT(tnsPath + " deploy ios --path TNS_App")
            assert ("Project successfully prepared" in output) 
            assert ("Project successfully built" in output)   
            assert ("Successfully deployed on device with identifier" in output)  
            assert (deviceId in output)
            sleep(10)
                        
            # Get list installed apps
            output = runAUT(tnsPath + " device list-applications --device " + deviceId)
            assert ("org.nativescript.TNSApp" in output)
                        
            # Start it via device command and verify app is running
            output = runAUT(tnsPath + " device run org.nativescript.TNSApp --device " + deviceId)            
            sleep(10)            
            
            # Stop logging and print it
            runAUT("ps -A | grep \"device " + deviceId + "\" | awk '{print $1}' | xargs kill -9")
            runAUT("cat deviceLog.txt")
        else:
            print "Prerequisites not met. This test requires at least one real ios device."
            assert (False) 