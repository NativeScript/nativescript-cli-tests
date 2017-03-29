"""
Helper for working with real devices
"""
import os
import time

from PIL import Image

from core.device.adb import Adb, ADB_PATH
from core.device.device_type import DeviceType
from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH


class Device(object):

    @staticmethod
    def __get_screen(device_type, device_id, file_name):
        """
        Get screenshot of mobile device and save it to file (inside data/temp folder).
        :param device_type: DeviceType enum value.
        :param device_id: Device identifier (example: `emulator-5554`).
        :param file_name: Name of image that will be saved.
        :return: Fill file path where image is saved.
        """
        file_path = os.path.join("data", "temp", "{0}.png".format(file_name))
        File.remove(file_path)
        if (device_type == DeviceType.EMULATOR) or (device_type == DeviceType.ANDROID):
            # Cleanup sdcard
            output = Adb.run(command="shell rm /sdcard/*.png", device_id=device_id)
            if "Read-only file system" in output:
                Emulator.unlock_sdcard()
                output = Adb.run(command="shell rm /sdcard/*.png", device_id=device_id)
                assert "error" not in output.lower(), "Screencap failed with: " + output

            # Get current screen of mobile device
            output = Adb.run(command="shell screencap -p /sdcard/{0}.png".format(file_name), device_id=device_id)
            if "Read-only file system" in output:
                Emulator.unlock_sdcard()
                output = Adb.run(command="shell screencap -p /sdcard/{0}.png".format(file_name), device_id=device_id)
                assert "error" not in output.lower(), "Screencap failed with: " + output

            # Transfer image from device to localhost
            output = Adb.run(command="pull /sdcard/{0}.png {1}".format(file_name, file_path), device_id=device_id)
            assert "100%" in output, "Failed to get {0}. Log: {1}".format(file_name, output)

            # Cleanup sdcard
            Adb.run(command="shell rm /sdcard/{0}.png".format(file_name), device_id=device_id)

        if device_type == DeviceType.SIMULATOR:
            run(command="xcrun simctl io booted screenshot {0}".format(file_path),
                log_level=CommandLogLevel.SILENT)
        if device_type == DeviceType.IOS:
            run(command="idevicescreenshot -u {0} {1}.tiff".format(device_id, file_name),
                log_level=CommandLogLevel.SILENT)
            run(command="sips -s format png {0}.tiff --out {1}".format(file_name, file_path),
                log_level=CommandLogLevel.SILENT)
            File.remove("{0}.tiff".format(file_name))
        return file_path

    @staticmethod
    def __image_match(actual_image_path, expected_image_path, tolerance=0.05):
        """
        Compare two images.
        :param actual_image_path: Path to actual image.
        :param expected_image_path: Path to expected image.
        :return: match (boolean value), diff_percent (diff %), diff_image (diff image)
        """
        actual_image = Image.open(actual_image_path)
        actual_pixels = actual_image.load()
        expected_image = Image.open(expected_image_path)
        expected_pixels = expected_image.load()
        width, height = expected_image.size

        total_pixels = width * height
        diff_pixels = 0
        match = False
        diff_image = actual_image.copy()
        for x in range(0, width):
            for y in range(40, height):
                if actual_pixels[x, y] != expected_pixels[x, y]:
                    diff_pixels += 1
                    diff_image.load()[x, y] = (255, 0, 0)

        diff_percent = 100 * float(diff_pixels) / total_pixels
        if diff_percent < tolerance:
            match = True

        return match, diff_percent, diff_image

    @staticmethod
    def screen_match(device_type, device_name, device_id, expected_image, tolerance=0.05, timeout=60):
        """
        Verify screen match expected image.
        :param device_type: DeviceType value.
        :param device_name: Name of device (name of Android avd image, or name or iOS Simulator).
        :param device_id: Device identifier (example: `emulator-5554`).
        :param expected_image: Name of expected image.
        :param timeout: Timeout in secconds.
        """
        print "Verify {0} looks correct...".format(expected_image)
        expected_image_path = os.path.join("data", "images", device_name, "{0}.png".format(expected_image))
        if File.exists(expected_image_path):
            t_end = time.time() + timeout
            diff = 100.0
            are_equal = False
            comparison_result = None
            while time.time() < t_end:
                actual_image_name = expected_image
                actual_image_path = Device.__get_screen(device_type, device_id, actual_image_name)
                if File.exists(actual_image_path):
                    comparison_result = Device.__image_match(actual_image_path, expected_image_path, tolerance)
                    are_equal = comparison_result[0]
                    diff = comparison_result[1]
                    if are_equal:
                        print "{0} looks OK.".format(expected_image)
                        break
                    else:
                        time.sleep(2)
                        print "{0} does not match. Diff is {1} %. Wait...".format(expected_image, diff)
            if not are_equal:
                base_file_name = actual_image_path.rsplit("/")[-1]
                actual_file_name = "actual_{0}".format(base_file_name)
                expected_file_name = "expected_{0}".format(base_file_name)
                diff_file_name = "diff_{0}".format(base_file_name)
                File.copy(actual_image_path, os.path.join("out", actual_file_name))
                File.copy(expected_image_path, os.path.join("out", expected_file_name))
                comparison_result[2].save(os.path.join("out", diff_file_name))
            assert are_equal, "Current image on {0} does not match expected image {1}. Diff is {2}%". \
                format(device_name, expected_image, diff)
        else:
            print "Expected image not found. Actual image will be saved as expected."
            time.sleep(timeout)
            actual_image_name = expected_image
            actual_image_path = Device.__get_screen(device_type, device_id, actual_image_name)
            file_name = actual_image_path.rsplit("/")[-1]
            File.copy(actual_image_path, os.path.join("data", "images", device_name, file_name))

    @staticmethod
    def ensure_available(platform):
        """
        Ensure device is available.
        :param platform:
        """
        count = Device.get_count(platform)
        if count > 0:
            print "{0} {1} devices are running".format(count, platform)
        else:
            raise TypeError("No real devices attached to this host.")

    @staticmethod
    def get_id(platform):
        """Get Id of first connected physical device"""
        device_list = Device.get_ids(platform)
        return device_list.pop(0)

    @staticmethod
    def get_ids(platform):
        """
        Get IDs of all connected physical devices
        :param platform: 
        :return:
        """
        device_ids = list()
        output = run(TNS_PATH + " device", log_level=CommandLogLevel.SILENT)
        lines = output.splitlines()
        for line in lines:
            if (platform.lower() in line.lower()) and ('Emulator' not in line):
                device_id = line.split("\xe2\x94\x82")[4].replace(" ", "")
                print "{0} device with id {1} found.".format(platform, device_id)
                device_ids.append(device_id)
        return device_ids

    @staticmethod
    def get_count(platform=""):
        """Get physical device count"""
        device_ids = Device.get_ids(platform)
        return len(device_ids)

    @staticmethod
    def uninstall_app(app_prefix, platform, fail=True):
        """Uninstall mobile app"""
        if platform == "android":
            device_ids = Device.get_ids(platform)
            for device_id in device_ids:
                output = run(ADB_PATH + " -s {0} shell pm list packages -3".format(device_id), timeout=120)
                lines = output.splitlines()
                for line in lines:
                    if app_prefix in line:
                        app_name = line.split(":")[1]
                        app_name = app_name.replace(" ", "")
                        uninstall_result = run(ADB_PATH + " -s {0} shell pm uninstall {1}".format(device_id, app_name),
                                               timeout=120)
                        if "Success" in uninstall_result:
                            print "{0} application successfully uninstalled.".format(app_prefix)
                        else:
                            if fail:
                                raise NameError("{0} application failed to uninstall.".format(app_prefix))
        else:
            device_ids = Device.get_ids(platform)
            for device_id in device_ids:
                output = run("ideviceinstaller -u {0} -l".format(device_id), timeout=120)
                lines = output.splitlines()
                for line in lines:
                    if app_prefix in line:
                        app_name = line.split("-")[0]
                        app_name = app_name.replace(" ", "")
                        uninstall_result = run("ideviceinstaller -u {0} -U {1}".format(device_id, app_name),
                                               timeout=120)
                        if "Uninstall: Complete" in uninstall_result:
                            print "{0} application successfully uninstalled.".format(app_prefix)
                        else:
                            if fail:
                                raise NameError("{0} application failed to uninstall.".format(app_prefix))

    @staticmethod
    def stop_application(device_id, app_id):
        """Stop application"""
        output = run(ADB_PATH + " -s " + device_id + " shell am force-stop " + app_id)
        time.sleep(5)
        assert app_id not in output, "Failed to stop " + app_id

    @staticmethod
    def is_running(app_id, device_id):
        """Check if app is running"""
        output = run(ADB_PATH + " -s " + device_id + " shell ps | grep " + app_id)
        if app_id in output:
            return True
        else:
            return False

    @staticmethod
    def wait_until_app_is_running(app_id, device_id, timeout=60):
        """
        Wait until app is running.
        :param app_id: Bundle identifier, for example: org.nativescript.TNSApp
        :param device_id: Device identifier.
        :param timeout: Timeout in seconds.
        """
        running = False
        end_time = time.time() + timeout
        while not running:
            time.sleep(5)
            running = Device.is_running(app_id, device_id)
            if running:
                print '{0} is running on {1}'.format(app_id, device_id)
                break
            if (running is False) and (time.time() > end_time):
                raise NameError('{0} is NOT running on {1}'.format(app_id, device_id))
