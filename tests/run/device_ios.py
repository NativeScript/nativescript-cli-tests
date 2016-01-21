"""
Test for device command in context of iOS
"""

import unittest
from time import sleep

from core.device.device import Device
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, ANDROID_RUNTIME_PATH, IOS_RUNTIME_SYMLINK_PATH
from core.tns.tns import Tns


class DeviceiOS(unittest.TestCase):
    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')
        Device.ensure_available(platform="ios")

    def tearDown(self):
        pass

    def test_001_device_log_list_applications_and_run_android(self):

        device_id = Device.get_id(platform="android")
        if device_id is not None:

            # Start DeviceLog
            run(TNS_PATH + " device log --device " + device_id + " > deviceLog.txt &", None, False)

            # Deploy TNS_App on device
            Tns.create_app_platform_add(
                    app_name="TNS_App",
                    platform="android",
                    framework_path=ANDROID_RUNTIME_PATH)
            output = run(TNS_PATH + " deploy android --path TNS_App --justlaunch")
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device" in output
            assert device_id in output
            sleep(10)

            # Verify "tns device list-applications" list org.nativescript.TNSApp
            output = run(TNS_PATH + " device list-applications --device " + device_id)
            assert "org.nativescript.TNSApp" in output

            # Verify app is running
            Device.wait_until_app_is_running(
                    app_id="org.nativescript.TNSApp",
                    device_id=device_id,
                    timeout=60)

            # Kill the app
            Device.stop_application(app_id="org.nativescript.TNSApp", device_id=device_id)

            # Start it via device command and verify app is running
            run(TNS_PATH + " device run org.nativescript.TNSApp --device " + device_id + " --justlaunch")

            # Verify app is running
            Device.wait_until_app_is_running(
                    app_id="org.nativescript.TNSApp",
                    device_id=device_id,
                    timeout=60)

            # Stop logging and print it
            run("ps -A | grep \"device " + device_id +
                "\" | awk '{print $1}' | xargs kill -9")
            run("cat deviceLog.txt")
        else:
            print "Prerequisites not met. This test requires at least one real android device."
            assert False

    def test_002_device_log_list_applications_and_run_ios(self):
        device_id = Device.get_id(platform="ios")
        if device_id is not None:

            # Start DeviceLog
            run(TNS_PATH + " device log --device " + device_id + " > deviceLog.txt &", None, False)

            # Deploy TNS_App on device
            Tns.create_app_platform_add(
                    app_name="TNS_App",
                    platform="ios",
                    framework_path=IOS_RUNTIME_SYMLINK_PATH,
                    symlink=True)
            output = run(TNS_PATH + " deploy ios --path TNS_App --justlaunch")
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device" in output
            assert device_id in output
            sleep(10)

            # Get list installed apps
            output = run(TNS_PATH + " device list-applications --device " + device_id)
            assert "org.nativescript.TNSApp" in output

            # Start it via device command and verify app is running
            run(TNS_PATH + " device run org.nativescript.TNSApp --device " + device_id + " --justlaunch")
            sleep(10)

            # Stop logging and print it
            run("ps -A | grep \"device " + device_id +
                "\" | awk '{print $1}' | xargs kill -9")
            run("cat deviceLog.txt")
        else:
            print "Prerequisites not met. This test requires at least one real ios device."
            assert False
