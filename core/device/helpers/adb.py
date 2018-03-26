"""
Wrapper around adb
"""
import os
import re
import time

from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS, EMULATOR_ID

ANDROID_HOME = os.environ.get('ANDROID_HOME')
ADB_PATH = os.path.join(ANDROID_HOME, 'platform-tools', 'adb')


class Adb(object):
    @staticmethod
    def __find_aapt():
        """
        Find aapt tool under $ANDRODI_HOME/build-tools
        :return: Path to appt.
        """
        aapt_executable = 'aapt'
        if CURRENT_OS is OSType.WINDOWS:
            aapt_executable += '.exe'
        base_path = os.path.join(ANDROID_HOME, 'build-tools')
        return File.find(base_path=base_path, file_name=aapt_executable, exact_match=True)

    @staticmethod
    def __get_package_id(apk_file):
        """
        Get package id from apk file.
        :param apk_file: Path to apk file.
        :return: Package identifier.
        """
        app_id = None
        aapt = Adb.__find_aapt()
        command = aapt + ' dump badging ' + apk_file
        output = run(command=command, log_level=CommandLogLevel.COMMAND_ONLY)
        for line in output.split('\n'):
            if 'package:' in line:
                app_id = line.split('\'')[1]
        return app_id

    @staticmethod
    def get_devices(include_emulators=False):
        """
        Get available android devices (only real devices).
        """
        devices = list()
        output = run(ADB_PATH + ' devices -l')
        '''
        Example output:
        emulator-5554          device product:sdk_x86 model:Android_SDK_built_for_x86 device:generic_x86
        HT46BWM02644           device usb:336592896X product:m8_google model:HTC_One_M8 device:htc_m8
        '''
        for line in output.splitlines():
            if 'model' in line and ' device ' in line:
                device_id = line.split(' ')[0]
                devices.append(device_id)
        return devices

    @staticmethod
    def get_logcat(device_id):
        """
        Dump the log and then exit (don't block).
        :param device_id: Device id.
        """
        return Adb.run(command='logcat -d', device_id=device_id)

    @staticmethod
    def clear_logcat(device_id):
        """
        Clear (flush) the entire log and exit.
        :param device_id: Device id.
        """
        Adb.run(command='logcat -c', device_id=device_id)
        print "The logcat on {0} is cleared.".format(device_id)

    @staticmethod
    def get_start_time(device_id, app_id):
        """
        Get start time of application.
        :param device_id: Device id.
        :param app_id: App id.
        :return: Start time as string.
        """
        command = 'logcat -d | grep \'Displayed {0}\''.format(app_id)
        output = Adb.run(command=command, device_id=device_id, log_level=CommandLogLevel.SILENT)
        # Example: I/ActivityManager(19531): Displayed org.nativescript.TestApp/com.tns.NativeScriptActivity: +3s452ms
        if len(output) > 0:
            print "Start time: {0}.".format(output)

            start_time = output.rsplit("+")[1]
            print "Start time: {0}.".format(start_time)

            numbers = map(int, re.findall('\d+', start_time))
            num_len = len(str(numbers[-1]))
            if num_len == 1:
                numbers[1] = '00' + str(numbers[1])
            elif num_len == 2:
                numbers[1] = '0' + str(numbers[1])

            result = ''.join(str(x) for x in numbers)
            print "Start time: {0}.".format(result)
            return result
        else:
            raise IOError('{0} has not displayed its activity - the app crashed!'.format(app_id))

    @staticmethod
    def run(command, device_id, timeout=60, log_level=CommandLogLevel.COMMAND_ONLY):
        """
        Run adb command.
        :param command: Command to run (without adb in front).
        :param device_id: Device id.
        :param timeout: Timeout.
        :param log_level: Log level.
        :return: Output of executed command.
        """
        return run(ADB_PATH + ' -s ' + device_id + ' ' + command, timeout=timeout, log_level=log_level)

    @staticmethod
    def uninstall_all_apps(device_id):
        """
        Uninstall all 3rd party applications.
        :param device_id: Device id.
        """
        print 'Uninstall all apps on {0}.'.format(device_id)
        apps = Adb.run(command='shell pm list packages -3', device_id=device_id)
        for line in apps.splitlines():
            if 'package:' in line:
                app = line.replace('package:', '')
                Adb.uninstall(app_id=app, device_id=device_id)

    @staticmethod
    def install(apk_file_path, device_id):
        """
        Install application.
        :param apk_file_path: File path to .apk.
        :param device_id: Device id.
        """
        output = Adb.run(command='install -r ' + apk_file_path, device_id=device_id)
        assert 'Success' in output, 'Failed to install {0}. Output: {1}'.format(apk_file_path, output)
        print '{0} installed successfully on {1}.'.format(apk_file_path, device_id)

    @staticmethod
    def uninstall(app_id, device_id, assert_success=True):
        """
        Uninstall application.
        :param app_id: Package identifier - org.nativescript.testapp.
        :param device_id: Device id.
        """
        output = Adb.run(command='uninstall ' + app_id, device_id=device_id, log_level=CommandLogLevel.FULL)
        if assert_success:
            assert 'Success' in output, 'Failed to uninstall {0}. Output: {1}'.format(app_id, output)
            print '{0} uninstalled successfully from {1}.'.format(app_id, device_id)

    @staticmethod
    def start_app(device_id, app_id):
        """
        Start application.
        :param device_id: Device id.
        :param app_id: App id.
        """
        command = 'shell monkey -p ' + app_id + ' -c android.intent.category.LAUNCHER 1'
        output = Adb.run(command=command, device_id=device_id)
        assert 'Events injected: 1' in output, 'Failed to start {0}.'.format(app_id)
        print '{0} started successfully.'.format(app_id)

    @staticmethod
    def stop_application(device_id, app_id):
        """
        Stop application
        :param device_id: Device identifier
        :param app_id: Bundle identifier (example: org.nativescript.TestApp)
        """
        command = ADB_PATH + " -s " + device_id + " shell am force-stop " + app_id
        output = run(command=command, log_level=CommandLogLevel.FULL)
        time.sleep(5)
        assert app_id not in output, "Failed to stop " + app_id
        time.sleep(5)

    @staticmethod
    def is_application_running(device_id, app_id):
        """
        Check if app is running.
        :param app_id: Bundle identifier (example: org.nativescript.TestApp)
        :param device_id: Device identifier
        :return: True if application is running
        """
        command = ADB_PATH + " -s " + device_id + " shell ps | grep -i " + app_id
        output = run(command=command, log_level=CommandLogLevel.SILENT)
        if app_id in output:
            return True
        else:
            return False

    @staticmethod
    def monkey(apk_file, device_id):
        """
        Perform monkey testing.
        :param apk_file: Application under test.
        :param device_id: Device id.
        """
        Adb.__monkey_kill(device_id)
        app_id = Adb.__get_package_id(apk_file)
        print 'Start monkey testing...'
        output = Adb.run(command='shell monkey -p ' + app_id + ' --throttle 100 -v 100 -s 120', device_id=device_id)
        assert 'No activities found' not in output, '{0} is not available on {1}'.format(app_id, device_id)
        assert 'Monkey aborted due to error' not in output, '{0} crashed! \n Log: \n {1}'.format(app_id, output)
        assert 'Monkey finished' in output, 'Unknown error occurred! \n Log: \n {0}'.format(output)
        print 'Monkey test passed!'

    @staticmethod
    def __monkey_kill(device_id):
        """
        Kill running adb monkey instances.
        :param device_id: device id.
        """
        kill_command = "shell ps | awk '/com\.android\.commands\.monkey/ { system(\"adb shell kill \" $2) }'"
        Adb.run(command=kill_command, device_id=device_id, log_level=CommandLogLevel.SILENT)

    @staticmethod
    def __list_path(device_id, package_id, path):
        """
        List file of application.
        :param device_id: Device identifier.
        :param package_id: Package identifier.
        :param path: Path relative to root folder of the package.
        :return: List of files and folders
        """
        command = 'shell run-as {0} ls -la /data/data/{1}/files/{2}'.format(package_id, package_id, path)
        output = Adb.run(command=command, device_id=device_id, log_level=CommandLogLevel.FULL)
        return output

    @staticmethod
    def path_exists(device_id, package_id, path, timeout=20):
        """
        Wait until path exists (relative based on folder where package is deployed) on emulator/android device.
        :param device_id: Device identifier.
        :param package_id: Package identifier.
        :param path: Relative path (based on folder where pacakge is deployed).
        :param timeout: Timeout in seconds.
        :return: True if path exists, false if path does not exists
        """
        t_end = time.time() + timeout
        found = False
        while time.time() < t_end:
            files = Adb.__list_path(device_id=device_id, package_id=package_id, path=path)
            if 'No such file or directory' not in files:
                found = True
                break
        return found

    @staticmethod
    def path_does_not_exist(device_id, package_id, path, timeout=20):
        """
        Wait until path does not exist (relative based on folder where package is deployed) on emulator/android device.
        :param device_id: Device identifier.
        :param package_id: Package identifier.
        :param path: Relative path (based on folder where pacakge is deployed).
        :param timeout: Timeout in seconds.
        :return: True if path does not exist, false if path exists
        """
        t_end = time.time() + timeout
        found = True
        while time.time() < t_end:
            files = Adb.__list_path(device_id=device_id, package_id=package_id, path=path)
            if 'No such file or directory' in files:
                found = False
                break
        return not found

    @staticmethod
    def get_page_source(device_id):
        """
        Get UI Tree as XML document
        :param device_id: Device identifier.
        :return: XML document with UI tree.
        """
        remove_command = 'shell rm -rf /sdcard/view.xml'
        get_source_command = 'shell uiautomator dump /sdcard/view.xml'
        read_source_command = 'shell cat /sdcard/view.xml'
        Adb.run(command=remove_command, device_id=device_id, log_level=CommandLogLevel.SILENT)
        Adb.run(command=get_source_command, device_id=device_id, log_level=CommandLogLevel.SILENT)
        output = Adb.run(command=read_source_command, device_id=device_id, log_level=CommandLogLevel.SILENT)
        return output

    @staticmethod
    def wait_for_text(device_id, text, timeout=20):
        """
        WAit until text is available on the screen of device.
        :param device_id: Device identifier.
        :param text: Desired text.
        :param timeout: Timeout in seconds.
        :return: True if text exists, false if text does not exists.
        """
        t_end = time.time() + timeout
        found = False
        while time.time() < t_end:
            source = Adb.get_page_source(device_id=device_id)
            if text in source:
                print '{0} found on current screen of {1}'.format(text, device_id)
                found = True
                break
        if not found:
            print '{0} NOT found on current screen of {1}'.format(text, device_id)
        return found

    @staticmethod
    def get_screen(device_id, file_path):
        """
        Save screen of mobile device.
        :param device_id: Device identifier (example: `emulator-5554`).
        :param file_path: Name of image that will be saved.
        """

        base_path, file_name = os.path.split(file_path)
        file_name = file_name.rsplit('.', 1)[0]

        # Cleanup sdcard
        output = Adb.run(command="shell rm /sdcard/*.png", device_id=device_id)
        if "Read-only file system" in output:
            Adb.unlock_sdcard(device_id=EMULATOR_ID)
            output = Adb.run(command="shell rm /sdcard/*.png", device_id=device_id)
            assert "error" not in output.lower(), "Screencap failed with: " + output
        # Get current screen of mobile device
        output = Adb.run(command="shell screencap -p /sdcard/{0}.png".format(file_name), device_id=device_id)
        if "Read-only file system" in output:
            Adb.unlock_sdcard(device_id=EMULATOR_ID)
            output = Adb.run(command="shell screencap -p /sdcard/{0}.png".format(file_name), device_id=device_id)
            assert "error" not in output.lower(), "Screencap failed with: " + output
        # Transfer image from device to localhost
        output = Adb.run(command="pull /sdcard/{0}.png {1}".format(file_name, file_path), device_id=device_id)
        assert "100%" in output, "Failed to get {0}. Log: {1}".format(file_name, output)
        # Cleanup sdcard
        Adb.run(command="shell rm /sdcard/{0}.png".format(file_name), device_id=device_id)

    @staticmethod
    def unlock_sdcard(device_id, timeout=60):
        """
        Unlock sdcard of default emulator.
        :param device_id: Device identifier (example: `emulator-5554`).
        :param timeout: Timeout in seconds.
        """
        t_end = time.time() + timeout
        unlocked = False
        while time.time() < t_end:
            output = Adb.run('shell mount -o remount rw /sdcard', device_id=device_id, log_level=CommandLogLevel.FULL)
            if 'mount' not in output:
                unlocked = True
                break
            else:
                print 'Failed to unlock sdcard. Retry...'
                time.sleep(10)
        assert unlocked, 'Failed to unlock sdcard!'

    @staticmethod
    def turn_on_screen(device_id):
        """
        Turn on screen.
        :param device_id: Device identifier
        """
        cmd_key_event = ADB_PATH + " -s " + device_id + " shell input keyevent 26"
        cmd_input_method = ADB_PATH + " -s " + device_id + " shell dumpsys input_method | grep mActive"

        output = run(command=cmd_input_method, log_level=CommandLogLevel.SILENT)
        is_active = "mActive=true" in output

        if is_active:
            print "The screen is already active."
            run(command=cmd_key_event, log_level=CommandLogLevel.SILENT)
            time.sleep(1)
            output = run(command=cmd_input_method, log_level=CommandLogLevel.SILENT)
            assert "mActive=false" in output
            time.sleep(1)
            run(command=cmd_key_event)
            time.sleep(1)
            output = run(command=cmd_input_method, log_level=CommandLogLevel.SILENT)
            assert "mActive=true" in output
        else:
            print "The screen is not active. Turn it on..."
            run(command=cmd_key_event)
            time.sleep(1)
            output = run(command=cmd_input_method, log_level=CommandLogLevel.SILENT)
            assert "mActive=true" in output
