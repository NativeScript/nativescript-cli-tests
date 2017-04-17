"""
Helper for working with real devices
"""
import os
import time

from core.device.adb import Adb, ADB_PATH
from core.device.device_type import DeviceType
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.image_utils import ImageUtils
from core.settings.settings import OUTPUT_FOLDER
from core.tns.tns_platform_type import Platform


class Device(object):
    @staticmethod
    def __get_device_type(device_id):
        """
        Get device type based on device id.
        :param device_id: Device identifier.
        :return: DeviceType enum value.
        """
        if len(device_id) < 30:
            if 'emu' in device_id:
                return DeviceType.EMULATOR
            else:
                return DeviceType.ANDROID
        else:
            if '-' in device_id:
                return DeviceType.SIMULATOR
            else:
                return DeviceType.IOS

    @staticmethod
    def get_screen(device_type, device_id, file_path):
        """
        Save screen of mobile device.
        :param device_type: DeviceType enum value.
        :param device_id: Device identifier (example: `emulator-5554`).
        :param file_path: Name of image that will be saved.
        """

        File.remove(file_path)
        base_path, file_name = os.path.split(file_path)
        file_name = file_name.rsplit('.', 1)[0]
        Folder.create(base_path)

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

    @staticmethod
    def screen_match(device_type, device_name, device_id, expected_image, tolerance=0.05, timeout=60):
        """
        Verify screen match expected image.
        :param device_type: DeviceType value.
        :param device_name: Name of device (name of Android avd image, or name or iOS Simulator).
        :param device_id: Device identifier (example: `emulator-5554`).
        :param expected_image: Name of expected image.
        :param tolerance: Tolerance in percents.
        :param timeout: Timeout in seconds.
        """
        print "Verify {0} looks correct...".format(expected_image)
        expected_image_original_path = os.path.join("data", "images", device_name, "{0}.png".format(expected_image))
        actual_image_path = os.path.join(OUTPUT_FOLDER, "images", device_name, "{0}_actual.png".format(expected_image))
        diff_image_path = os.path.join(OUTPUT_FOLDER, "images", device_name, "{0}_diff.png".format(expected_image))
        expected_image_path = os.path.join(OUTPUT_FOLDER, "images", device_name,
                                           "{0}_expected.png".format(expected_image))

        if File.exists(expected_image_original_path):
            t_end = time.time() + timeout
            diff = 100.0
            are_equal = False
            comparison_result = None
            while time.time() < t_end:
                # Get actual screen
                if File.exists(actual_image_path):
                    File.remove(actual_image_path)
                Device.get_screen(device_type=device_type, device_id=device_id, file_path=actual_image_path)

                # Compare with expected image
                if File.exists(actual_image_path):
                    comparison_result = ImageUtils.image_match(actual_image_path=actual_image_path,
                                                               expected_image_path=expected_image_original_path,
                                                               tolerance=tolerance)
                    are_equal = comparison_result[0]
                    diff = comparison_result[1]
                    if are_equal:
                        print "{0} looks OK.".format(expected_image)
                        break # Exist if images look OK.
                    else:
                        time.sleep(2)
                        print "{0} does not match. Diff is {1} %. Wait...".format(expected_image, diff)
                else:
                    print "Failed to get image from {0}".format(device_id)

            # Report results after timeout is over
            if not are_equal:
                # Save expected and diff images (actual is already there)
                File.copy(src=expected_image_original_path, dest=expected_image_path)
                comparison_result[2].save(os.path.join("out", diff_image_path))
            assert are_equal, "Current image on {0} does not match expected image {1}. Diff is {2}%". \
                format(device_name, expected_image, diff)
        else:
            # If expected image is not found actual will be saved as expected.
            print "Expected image not found. Actual image will be saved as expected."
            time.sleep(timeout)
            Device.get_screen(device_type, device_id, expected_image_original_path)

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
        device_list = Device.get_ids(platform=platform)
        if len(device_list) > 0:
            return device_list.pop(0)
        else:
            error = 'No connected {0} real devices!'.format(platform)
            raise NameError(error)

    @staticmethod
    def get_ids(platform):
        """
        Get IDs of all connected physical devices
        :param platform: `Platform.ANDROID` or `Platform.IOS`
        :return:
        """
        device_ids = list()
        if platform is Platform.IOS:
            output = run(command='idevice_id --list', timeout=60, log_level=CommandLogLevel.SILENT)
            for line in output.splitlines():
                command = 'instruments -s | grep {0}'.format(line)
                check_connected = run(command=command, timeout=30, log_level=CommandLogLevel.SILENT)
                if 'null' not in check_connected:
                    device_ids.append(line)
                else:
                    message = '{0} is not trusted!'.format(line)
                    print message
        elif platform is Platform.ANDROID:
            device_ids = Adb.get_devices()
        else:
            raise NameError('Invalid platform')

        return device_ids

    @staticmethod
    def get_count(platform=Platform.BOTH):
        """Get physical device count"""
        device_ids = Device.get_ids(platform=platform)
        return len(device_ids)

    @staticmethod
    def uninstall_app(app_prefix, platform, fail=True):
        """Uninstall mobile app"""
        device_ids = Device.get_ids(platform=platform)
        if platform == Platform.ANDROID:
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
        elif platform == Platform.ANDROID:
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
        """
        Stop application
        :param device_id: Device identifier
        :param app_id: Bundle identifier (example: org.nativescript.TestApp)
        """
        device_type = Device.__get_device_type(device_id=device_id)
        if device_type is DeviceType.SIMULATOR:
            Simulator.stop_application(app_id=app_id)
        elif device_type is DeviceType.IOS:
            raise NotImplementedError
        else:
            output = run(ADB_PATH + " -s " + device_id + " shell am force-stop " + app_id)
            time.sleep(5)
            assert app_id not in output, "Failed to stop " + app_id

    @staticmethod
    def is_running(app_id, device_id):
        """
        Check if app is running.
        :param app_id: Bundle identifier (example: org.nativescript.TestApp)
        :param device_id: Device identifier
        :return: True if application is running
        """
        device_type = Device.__get_device_type(device_id=device_id)
        if device_type is DeviceType.SIMULATOR:
            raise NotImplementedError
        elif device_type is DeviceType.IOS:
            raise NotImplementedError
        else:
            output = run(ADB_PATH + " -s " + device_id + " shell ps | grep -i " + app_id)
            if app_id in output:
                return True
            else:
                return False

    @staticmethod
    def wait_until_app_is_running(app_id, device_id, timeout=60):
        """
        Wait until app is running.
        :param app_id: Bundle identifier (example: org.nativescript.TestApp)
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
