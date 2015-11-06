'''
Test for device command in context of iOS
'''
from time import sleep
import unittest

from helpers._os_lib import cleanup_folder, run_aut
from helpers._tns_lib import tnsPath, create_project_add_platform, \
    androidRuntimePath, iosRuntimeSymlinkPath
from helpers.adb import stop_application, wait_until_app_is_running
from helpers.device import given_real_device, get_physical_device_id

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

        cleanup_folder('./TNS_App')
        given_real_device(platform="ios")

    def tearDown(self):
        pass

    def test_001_Device_Log_ListApplications_And_Run_Android(self):

        device_id = get_physical_device_id(platform="android")
        if device_id is not None:

            # Start DeviceLog
            run_aut(
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
            output = run_aut(tnsPath + " deploy android --path TNS_App")
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device" in output
            assert device_id in output
            sleep(10)

            # VErify "tns device list-applications" list
            # org.nativescript.TNSApp
            output = run_aut(
                tnsPath +
                " device list-applications --device " +
                device_id)
            assert "org.nativescript.TNSApp" in output

            # Verify app is running
            wait_until_app_is_running(
                app_id="org.nativescript.TNSApp",
                device_id=device_id,
                timeout=60)

            # Kill the app
            stop_application(app_id="org.nativescript.TNSApp", device_id=device_id)

            # Start it via device command and verify app is running
            run_aut(
                tnsPath +
                " device run org.nativescript.TNSApp --device " +
                device_id)

            # Verify app is running
            wait_until_app_is_running(
                app_id="org.nativescript.TNSApp",
                device_id=device_id,
                timeout=60)

            # Stop logging and print it
            run_aut("ps -A | grep \"device " + device_id +
                   "\" | awk '{print $1}' | xargs kill -9")
            run_aut("cat deviceLog.txt")
        else:
            print "Prerequisites not met. This test requires at least one real android device."
            assert False

    def test_002_Device_Log_ListApplications_And_Run_iOS(self):
        device_id = get_physical_device_id(platform="ios")
        if device_id is not None:

            # Start DeviceLog
            run_aut(
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
            output = run_aut(tnsPath + " deploy ios --path TNS_App")
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device" in output
            assert device_id in output
            sleep(10)

            # Get list installed apps
            output = run_aut(
                tnsPath +
                " device list-applications --device " +
                device_id)
            assert "org.nativescript.TNSApp" in output

            # Start it via device command and verify app is running
            output = run_aut(
                tnsPath +
                " device run org.nativescript.TNSApp --device " +
                device_id)
            sleep(10)

            # Stop logging and print it
            run_aut("ps -A | grep \"device " + device_id +
                   "\" | awk '{print $1}' | xargs kill -9")
            run_aut("cat deviceLog.txt")
        else:
            print "Prerequisites not met. This test requires at least one real ios device."
            assert False
