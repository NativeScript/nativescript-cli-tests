from time import sleep
import unittest

from helpers._os_lib import CleanupFolder, runAUT, KillProcess
from helpers._tns_lib import CreateProjectAndAddPlatform, iosRuntimeSymlinkPath, \
    tnsPath
from helpers.device import GivenRealDeviceRunning


class Debug_OSX(unittest.TestCase):

    def setUp(self):
        
        print ""
        
        CleanupFolder('./TNS_App');
        GivenRealDeviceRunning(platform="ios")
        
        KillProcess("Safari")
        KillProcess("iOS Simulator")
        runAUT("ideviceinstaller -U org.nativescript.TNSApp")

    def tearDown(self):        
        KillProcess("Safari")
        KillProcess("iOS Simulator")

        runAUT("ideviceinstaller -U org.nativescript.TNSApp")
    
    def test_001_Debug_iOS_Simulator_DebugBrk(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath)     
        output = runAUT(tnsPath + " debug ios --debug-brk --emulator --path TNS_App --frameworkPath " + iosRuntimeSymlinkPath, 2*60, True)
        assert ("Project successfully prepared" in output) 
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Starting iOS Simulator" in output)
        assert ("Frontend client connected" in output)
        assert ("Session started without errors" in output)
        assert ("Backend socket created" in output)
        assert not ("closed" in output)
        assert not ("detached" in output)
        assert not ("disconnected" in output)
    
    def test_002_Debug_iOS_Simulator_Start(self):

        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath)   
        output = runAUT(tnsPath + " emulate ios --path TNS_App --justlaunch")  
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Starting iOS Simulator" in output)
        assert ("Session started without errors" in output)
        sleep(10)
        output = runAUT(tnsPath + " debug ios --start --emulator --path TNS_App --frameworkPath " + iosRuntimeSymlinkPath, 2*60, True)
        assert ("Setting up debugger proxy..." in output)
        assert ("Frontend client connected" in output)
        assert ("Backend socket created" in output)
        assert not ("Backend socket closed" in output)
        assert not ("Frontend socket closed" in output)
        assert not ("closed" in output)
        assert not ("detached" in output)
        assert not ("disconnected" in output)

    def test_003_Debug_iOS_Device_DebugBrk(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath)     
        output = runAUT(tnsPath + " debug ios --debug-brk --path TNS_App --timeout 120 --frameworkPath " + iosRuntimeSymlinkPath, 3*60, True)
        assert ("Project successfully prepared" in output) 
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Successfully deployed on device " in output)
        assert ("Successfully run application org.nativescript.TNSApp on device with ID" in output)
        assert ("NativeScript waiting for debugger" in output)
        assert ("Setting up debugger proxy..." in output)
        assert ("Opened localhost 8080" in output)
        assert ("Frontend client connected" in output)
        assert ("Backend socket created" in output)
        assert ("NativeScript debugger attached" in output)
        assert not ("closed" in output)
        assert not ("detached" in output)
        assert not ("disconnected" in output)
    
    def test_004_Debug_iOS_Device_Start(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath)   
        output = runAUT(tnsPath + " run ios --path TNS_App --justlaunch")  
        assert ("** BUILD SUCCEEDED **" in output)
        assert ("Successfully deployed on device " in output)
        sleep(10)
        output = runAUT(tnsPath + " debug ios --start --path TNS_App --timeout 120 --frameworkPath " + iosRuntimeSymlinkPath, 2*60, True)
        assert ("Setting up debugger proxy..." in output)
        assert ("Frontend client connected" in output)
        assert ("Backend socket created" in output)
        assert not ("closed" in output)
        assert not ("detached" in output)
        assert not ("disconnected" in output) 