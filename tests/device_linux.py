'''
Test for device command in context of Android
'''
from time import sleep
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import tnsPath, create_project_add_platform, \
    androidRuntimePath
from helpers.adb import StopApplication, WaitUntilAppIsRunning
from helpers.device import GetDeviceCount, GetPhysicalDeviceId, \
    GivenRealDeviceRunning, GivenRunningEmulator

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0111, R0201, R0904
class DeviceAndroid(unittest.TestCase):

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
        device_id = GetPhysicalDeviceId(platform="android")
        if device_id is not None:

            # Deploy TNS_App on device
            create_project_add_platform(
                proj_name="TNS_App",
                platform="android",
                framework_path=androidRuntimePath)
            output = runAUT(tnsPath + " deploy android --path TNS_App")
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device with identifier" in output
            runAUT("echo " + device_id)
            assert device_id in output
            sleep(10)

            # Verify list-applications command list org.nativescript.TNSApp
            output = runAUT(
                tnsPath +
                " device list-applications --device " +
                device_id)
            assert "com.android." in output
            assert "com.google." in output
            assert "org.nativescript.TNSApp" in output

            # Verify app is running
            WaitUntilAppIsRunning(app_id="org.nativescript.TNSApp", device_id=device_id, timeout=60)

            # Kill the app
            StopApplication(app_id="org.nativescript.TNSApp", device_id=device_id)

            # Start via run command and verify it is running
            runAUT(tnsPath + " device run org.nativescript.TNSApp --device " + device_id)

            # Verify app is running
            WaitUntilAppIsRunning(app_id="org.nativescript.TNSApp", device_id=device_id, timeout=60)

        else:
            print "Prerequisites not met. This test requires at least one real android device."
            assert False

    def test_002_Device_Log_Android(self):
        if GetDeviceCount(platform="android") > 1:
            output = runAUT(tnsPath + " device log")
            assert "More than one device found. Specify device explicitly." in output
        else:
            print "Prerequisites not met. This test requires at least two attached devices."
            assert False

    def test_400_Device_InvalidPlatform(self):
        output = runAUT(tnsPath + " device windows")
        assert "'windows' is not a valid device platform." in output
        assert "Usage" in output

    def test_401_Device_Log_Invaliddevice_id(self):
        output = runAUT(tnsPath + " device log --device invaliddevice_id")
        assert "Cannot resolve the specified connected device by the provided index or identifier." in output
        assert "To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'." in output
        assert "Usage" in output

    def test_402_Device_Run_Invaliddevice_id(self):
        output = runAUT(tnsPath + " device run  --device invaliddevice_id")
        assert "Cannot resolve the specified connected device by the provided index or identifier." in output
        assert "To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'." in output
        assert "Usage" in output

    def test_403_Device_ListApplications_Invaliddevice_id(self):
        output = runAUT(
            tnsPath +
            " device list-applications --device invaliddevice_id")
        assert "Cannot resolve the specified connected device by the provided index or identifier." in output
        assert "To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'." in output
        assert "Usage" in output
