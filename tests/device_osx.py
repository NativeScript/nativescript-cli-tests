'''
Test for device command in context of iOS
'''
from time import sleep
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import tnsPath, create_project_add_platform, \
    androidRuntimePath, iosRuntimeSymlinkPath
from helpers.adb import StopApplication, WaitUntilAppIsRunning
from helpers.device import GivenRealDeviceRunning, GetPhysicalDeviceId

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0111, R0201, R0904
class DeviceiOS(unittest.TestCase):

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

        device_id = GetPhysicalDeviceId(platform="android")
        if device_id is not None:

            # Start DeviceLog
            runAUT(
                tnsPath +
                " device log --device " +
                device_id +
                " > deviceLog.txt &",
                None,
                False)

            # Deploy TNS_App on device
            create_project_add_platform(
                proj_name="TNS_App",
                platform="android",
                framework_path=androidRuntimePath)
            output = runAUT(tnsPath + " deploy android --path TNS_App")
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device" in output
            assert device_id in output
            sleep(10)

            # VErify "tns device list-applications" list
            # org.nativescript.TNSApp
            output = runAUT(
                tnsPath +
                " device list-applications --device " +
                device_id)
            assert "org.nativescript.TNSApp" in output

            # Verify app is running
            WaitUntilAppIsRunning(
                app_id="org.nativescript.TNSApp",
                device_id=device_id,
                timeout=60)

            # Kill the app
            StopApplication(app_id="org.nativescript.TNSApp", device_id=device_id)

            # Start it via device command and verify app is running
            runAUT(
                tnsPath +
                " device run org.nativescript.TNSApp --device " +
                device_id)

            # Verify app is running
            WaitUntilAppIsRunning(
                app_id="org.nativescript.TNSApp",
                device_id=device_id,
                timeout=60)

            # Stop logging and print it
            runAUT("ps -A | grep \"device " + device_id +
                   "\" | awk '{print $1}' | xargs kill -9")
            runAUT("cat deviceLog.txt")
        else:
            print "Prerequisites not met. This test requires at least one real android device."
            assert False

    def test_002_Device_Log_ListApplications_And_Run_iOS(self):
        device_id = GetPhysicalDeviceId(platform="ios")
        if device_id is not None:

            # Start DeviceLog
            runAUT(
                tnsPath +
                " device log --device " +
                device_id +
                " > deviceLog.txt &",
                None,
                False)

            # Deploy TNS_App on device
            create_project_add_platform(
                proj_name="TNS_App",
                platform="ios",
                framework_path=iosRuntimeSymlinkPath,
                symlink=True)
            output = runAUT(tnsPath + " deploy ios --path TNS_App")
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device" in output
            assert device_id in output
            sleep(10)

            # Get list installed apps
            output = runAUT(
                tnsPath +
                " device list-applications --device " +
                device_id)
            assert "org.nativescript.TNSApp" in output

            # Start it via device command and verify app is running
            output = runAUT(
                tnsPath +
                " device run org.nativescript.TNSApp --device " +
                device_id)
            sleep(10)

            # Stop logging and print it
            runAUT("ps -A | grep \"device " + device_id +
                   "\" | awk '{print $1}' | xargs kill -9")
            runAUT("cat deviceLog.txt")
        else:
            print "Prerequisites not met. This test requires at least one real ios device."
            assert False
