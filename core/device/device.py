"""
Helper for working with real devices
"""
import os
import time

import pytesseract
from PIL import Image

from core.device.device_type import DeviceType
from core.device.helpers.adb import Adb
from core.device.helpers.android_uiautomator import UIAuto
from core.device.helpers.libimobiledevice import IDevice
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
    def get_screen(device_id, file_path):
        """
        Save screen of mobile device.
        :param device_id: Device identifier (example: `emulator-5554`).
        :param file_path: Path to image that will be saved.
        """

        File.remove(file_path)
        base_path, file_name = os.path.split(file_path)
        Folder.create(base_path)

        device_type = Device.__get_device_type(device_id)
        if (device_type == DeviceType.EMULATOR) or (device_type == DeviceType.ANDROID):
            Adb.get_screen(device_id=device_id, file_path=file_path)
        if device_type == DeviceType.SIMULATOR:
            Simulator.get_screen(device_id=device_id, file_path=file_path)
        if device_type == DeviceType.IOS:
            IDevice.get_screen(device_id=device_id, file_path=file_path)

        image_saved = False
        if File.exists(file_path):
            size = os.path.getsize(file_path)
            if size > 10:
                image_saved = True
        return image_saved

    @staticmethod
    def screen_match(device_name, device_id, expected_image, tolerance=0.1, timeout=30):
        """
        Verify screen match expected image.
        :param device_name: Name of device (name of Android avd image, or name or iOS Simulator).
        :param device_id: Device identifier (example: `emulator-5554`).
        :param expected_image: Name of expected image.
        :param tolerance: Tolerance in percents.
        :param timeout: Timeout in seconds.
        """

        device_type = Device.__get_device_type(device_id)
        if device_type == DeviceType.IOS:
            type = run(command="ideviceinfo | grep ProductType", log_level=CommandLogLevel.SILENT)
            type = type.replace(',', '')
            type = type.replace('ProductType:', '').strip(' ')
            device_name = type

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
                time.sleep(1)
                if Device.get_screen(device_id=device_id, file_path=actual_image_path):
                    comparison_result = ImageUtils.image_match(actual_image_path=actual_image_path,
                                                               expected_image_path=expected_image_original_path,
                                                               tolerance=tolerance)
                    are_equal = comparison_result[0]
                    diff = comparison_result[1]
                    if are_equal:
                        print "{0} looks OK.".format(expected_image)
                        break  # Exist if images look OK.
                    else:
                        time.sleep(2)
                        print "{0} does not match. Diff is {1} %. Wait...".format(expected_image, diff)
                else:
                    print "Failed to get image from {0}".format(device_id)

            # Report results after timeout is over
            if not are_equal:
                # Save expected and diff images (actual is already there)
                diff_image_final_path = os.path.join("out", diff_image_path)
                print "Diff image will be saved at " + diff_image_final_path
                File.copy(src=expected_image_original_path, dest=expected_image_path)
                comparison_result[2].save(diff_image_final_path)
                # Get logs (from android devices).
                if device_type == DeviceType.EMULATOR or device_type == DeviceType.ANDROID:
                    log_path = diff_image_final_path.replace('_diff.png', '.log')
                    print "Console logs will be saved at " + log_path
                    log = Adb.get_logcat(device_id=device_id)
                    if len(log) < 10000:
                        print log
                    File.write(file_path=log_path, text=log)
            assert are_equal, "Current image on {0} does not match expected image {1}. Diff is {2}%". \
                format(device_name, expected_image, diff)
        else:
            # If expected image is not found actual will be saved as expected.
            print "Expected image not found. Actual image will be saved as expected: " + expected_image_original_path
            time.sleep(timeout)
            Device.get_screen(device_id, expected_image_original_path)
            assert False, "Expected image not found!"

    @staticmethod
    def get_screen_text(device_id):
        """
        Get text of current screen on mobile device.
        :param device_id: Device identifier (example: `emulator-5554`).
        :return: All the text visible on screen as string
        """
        img_name = "actual_{0}_{1}.png".format(device_id, time.time())
        actual_image_path = os.path.join(OUTPUT_FOLDER, "images", device_id, img_name)
        if File.exists(actual_image_path):
            File.remove(actual_image_path)
        Device.get_screen(device_id=device_id, file_path=actual_image_path)
        image = Image.open(actual_image_path).convert('LA')
        text = pytesseract.image_to_string(image)
        return text

    @staticmethod
    def get_log(device_id):
        """
        Dump the entire log.
        :param device_id: Device id.
        """
        device_type = Device.__get_device_type(device_id)
        if (device_type == DeviceType.EMULATOR) or (device_type == DeviceType.ANDROID):
            Adb.get_logcat(device_id)
        else:
            raise NotImplementedError('Not Implemented for iOS!')

    @staticmethod
    def get_start_time(device_id, app_id):
        """
        Get start time of application. Examples:
        - Android - I/ActivityManager(19531): Displayed org.nativescript.TestApp/com.tns.NativeScriptActivity: +3s452ms
        - iOS - TODO(vchimev)
        :param device_id: Device id.
        :param app_id: App id.
        :return: Start time.
        """
        device_type = Device.__get_device_type(device_id)
        if (device_type == DeviceType.EMULATOR) or (device_type == DeviceType.ANDROID):
            return Adb.get_start_time(device_id, app_id)
        else:
            raise NotImplementedError('Not Implemented for iOS!')

    @staticmethod
    def wait_for_text(device_id, text="", timeout=60):
        """
        Wait for text to be visible on screen of device.
        :param device_id: Device identifier (example: `emulator-5554`).
        :param text: Text that should be visible on the screen.
        :param timeout: Timeout in seconds.
        :return: True if text found, False if not found.
        """

        # IMPORTANT NOTE !!!!
        # UIAuto.wait_for_text() does not work well with cases when you specify partial text of element.
        # Example: Element text is "42 taps left" and you try to wait for "taps" string only
        # TODO: Think about some fix (may be xpath on view hierarchy)

        device_type = Device.__get_device_type(device_id)
        if device_type == DeviceType.ANDROID or device_type == DeviceType.EMULATOR:
            return Adb.wait_for_text(device_id=device_id, text=text, timeout=timeout)
        else:
            t_end = time.time() + timeout
            found = False
            actual_text = ""
            while time.time() < t_end:
                actual_text = Device.get_screen_text(device_id=device_id)
                if text in actual_text:
                    print text + " found on screen of " + device_id
                    found = True
                    break
                else:
                    print text + " NOT found on screen of " + device_id
                    time.sleep(5)
            if not found:
                print "ACTUAL TEXT:"
                print actual_text
            return found

    @staticmethod
    def clear_log(device_id):
        """
        Flush the entire log.
        :param device_id: Device id.
        """
        device_type = Device.__get_device_type(device_id)
        if (device_type == DeviceType.EMULATOR) or (device_type == DeviceType.ANDROID):
            Adb.clear_logcat(device_id)
        else:
            raise NotImplementedError('Not Implemented for iOS!')

    @staticmethod
    def click(device_id, text, timeout):
        """
        Click on text.
        :param device_id: Device identifier (example: `emulator-5554`).
        :param text: Text on where click will be performed.
        :param timeout: Timeout to find text before clicking it.
        """
        device_type = Device.__get_device_type(device_id)
        if (device_type == DeviceType.EMULATOR) or (device_type == DeviceType.ANDROID):
            UIAuto.click(device_id=device_id, text=text, timeout=timeout)
        else:
            raise NotImplementedError("Click on text not implemented for iOS devices and simulators.")

    @staticmethod
    def ensure_available(platform):
        """
        Ensure device is available.
        :param platform: `Platform.ANDROID` or `Platform.IOS`
        """
        count = Device.get_count(platform)
        if count > 0:
            print "{0} {1} device(s) attached.".format(count, platform)
        else:
            raise TypeError("No real devices attached.")

        # If device is Android, make sure /data/local/tmp is clean
        if platform == Platform.ANDROID:
            for device_id in Device.get_ids(platform=Platform.ANDROID, include_emulators=True):
                Adb.run(command="shell rm -rf /data/local/tmp/*", device_id=device_id, log_level=CommandLogLevel.FULL)

    @staticmethod
    def get_id(platform):
        """
        Get device identifier of first found physical device of given platform.
        :param platform: Platform enum value (Platform.ANDROID or Platform.IOS)
        :return: Device identifier.
        """
        device_list = Device.get_ids(platform=platform)
        if len(device_list) > 0:
            return device_list.pop(0)
        else:
            error = 'No connected {0} real devices!'.format(platform)
            raise NameError(error)

    @staticmethod
    def get_ids(platform, include_emulators=False):
        """
        Get IDs of all connected physical devices.
        :param platform: `Platform.ANDROID` or `Platform.IOS`
        :return: List of device identifiers.
        """
        if platform is Platform.IOS:
            return IDevice.get_devices()
        elif platform is Platform.ANDROID:
            return Adb.get_devices(include_emulators=include_emulators)
        else:
            raise NameError('Invalid platform')

    @staticmethod
    def get_count(platform):
        """
        Get physical device count.
        :param platform: `Platform.ANDROID` or `Platform.IOS`.
        :return: Count.
        """
        device_ids = Device.get_ids(platform=platform)
        return len(device_ids)

    @staticmethod
    def install_app(app_file_path, device_id):
        """
        Install application.
        :param app_file_path: File path to app.
        :param device_id: Device id.
        """
        device_type = Device.__get_device_type(device_id)
        if (device_type == DeviceType.EMULATOR) or (device_type == DeviceType.ANDROID):
            Adb.install(app_file_path, device_id)
        else:
            raise NotImplementedError('Not Implemented for iOS!')

    @staticmethod
    def uninstall_app(app_prefix, platform):
        """
        Uninstall all apps on all connected physical devices.
        :param app_prefix: App prefix, for example: org.nativescript.
        :param platform: Platform enum value (Platform.ANDROID or Platform.IOS)
        """
        device_ids = Device.get_ids(platform=platform, include_emulators=True)
        if platform == Platform.ANDROID:
            for device_id in device_ids:
                Adb.uninstall_all_apps(device_id=device_id)
                Adb.run(command="shell rm -rf /data/local/tmp/*", device_id=device_id, log_level=CommandLogLevel.FULL)
        elif platform == Platform.IOS:
            for device_id in device_ids:
                IDevice.uninstall_all_app(device_id=device_id, app_prefix=app_prefix)

    @staticmethod
    def start_app(device_id, app_id):
        """
        Start application.
        :param device_id: Device id.
        :param app_id: App id.
        """
        device_type = Device.__get_device_type(device_id)
        if (device_type == DeviceType.EMULATOR) or (device_type == DeviceType.ANDROID):
            Adb.start_app(device_id, app_id)
        else:
            raise NotImplementedError('Not Implemented for iOS!')

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
            Adb.stop_application(device_id=device_id, app_id=app_id)

    @staticmethod
    def is_running(device_id, app_id):
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
            Adb.is_application_running(device_id=device_id, app_id=app_id)

    @staticmethod
    def wait_until_app_is_running(device_id, app_id, timeout=60):
        """
        Wait until app is running.
        :param device_id: Device identifier.
        :param app_id: Bundle identifier (example: org.nativescript.TestApp)
        :param timeout: Timeout in seconds.
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            time.sleep(5)
            running = Device.is_running(device_id=device_id, app_id=app_id)
            if running:
                print '{0} is running on {1}'.format(app_id, device_id)
                break
            if (running is False) and (time.time() > end_time):
                raise NameError('{0} is NOT running on {1}'.format(app_id, device_id))

    @staticmethod
    def turn_on_screen(device_id):
        """
        Turn on screen.
        :param device_id: Device id.
        """
        device_type = Device.__get_device_type(device_id)
        if (device_type == DeviceType.EMULATOR) or (device_type == DeviceType.ANDROID):
            Adb.turn_on_screen(device_id)
        else:
            raise NotImplementedError('Not Implemented for iOS!')
