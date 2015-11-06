'''
Test for device command in context of Android
'''
from time import sleep
import unittest

from helpers._os_lib import cleanup_folder, run_aut
from helpers._tns_lib import TNSPATH, create_project_add_platform, \
    ANDROID_RUNTIME_PATH
from helpers.adb import stop_application, wait_until_app_is_running
from helpers.device import get_device_count, get_physical_device_id, \
    given_real_device, given_running_emulator

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

        cleanup_folder('./TNS_App')
        given_real_device(platform="android")
        given_running_emulator()

    def tearDown(self):
        pass

    def test_001_Device_ListApplications_And_Run_Android(self):
        device_id = get_physical_device_id(platform="android")
        if device_id is not None:

            # Deploy TNS_App on device
            create_project_add_platform(
                proj_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)
            output = run_aut(TNSPATH + " deploy android --path TNS_App")
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device with identifier" in output
            run_aut("echo " + device_id)
            assert device_id in output
            sleep(10)

            # Verify list-applications command list org.nativescript.TNSApp
            output = run_aut(
                TNSPATH +
                " device list-applications --device " +
                device_id)
            assert "com.android." in output
            assert "com.google." in output
            assert "org.nativescript.TNSApp" in output

            # Verify app is running
            wait_until_app_is_running(app_id="org.nativescript.TNSApp", device_id=device_id, timeout=60)

            # Kill the app
            stop_application(app_id="org.nativescript.TNSApp", device_id=device_id)

            # Start via run command and verify it is running
            run_aut(TNSPATH + " device run org.nativescript.TNSApp --device " + device_id)

            # Verify app is running
            wait_until_app_is_running(app_id="org.nativescript.TNSApp", device_id=device_id, timeout=60)

        else:
            print "Prerequisites not met. This test requires at least one real android device."
            assert False

    def test_002_Device_Log_Android(self):
        if get_device_count(platform="android") > 1:
            output = run_aut(TNSPATH + " device log")
            assert "More than one device found. Specify device explicitly." in output
        else:
            print "Prerequisites not met. This test requires at least two attached devices."
            assert False

    def test_400_Device_InvalidPlatform(self):
        output = run_aut(TNSPATH + " device windows")
        assert "'windows' is not a valid device platform." in output
        assert "Usage" in output

    def test_401_Device_Log_Invaliddevice_id(self):
        output = run_aut(TNSPATH + " device log --device invaliddevice_id")
        assert "Cannot resolve the specified connected device by the provided index or identifier." in output
        assert "To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'." in output
        assert "Usage" in output

    def test_402_Device_Run_Invaliddevice_id(self):
        output = run_aut(TNSPATH + " device run  --device invaliddevice_id")
        assert "Cannot resolve the specified connected device by the provided index or identifier." in output
        assert "To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'." in output
        assert "Usage" in output

    def test_403_Device_ListApplications_Invaliddevice_id(self):
        output = run_aut(
            TNSPATH +
            " device list-applications --device invaliddevice_id")
        assert "Cannot resolve the specified connected device by the provided index or identifier." in output
        assert "To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'." in output
        assert "Usage" in output
