import os
import time

from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS

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
    def __get_pacakge_id(apk_file):
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
        apps = Adb.run(command='shell pm list packages -3', device_id=device_id)
        for line in apps:
            if 'package:' in line:
                app = line.replace('package:', '')
                Adb.uninstall(app_id=app, device_id=device_id)

    @staticmethod
    def install(apk_file, device_id):
        """
        Install application.
        :param apk_file: Application under test.
        :param device_id: Device id.
        """
        output = Adb.run(command='install -r ' + apk_file, device_id=device_id)
        assert 'Success' in output, 'Failed to install {0}. \n Log: \n {1}'.format(apk_file, output)
        print '{0} installed successfully on {1}'.format(apk_file, device_id)

    @staticmethod
    def uninstall(app_id, device_id):
        """
        Uninstall application.
        :param app_id: Package identifier (for example org.nativescript.testapp).
        :param device_id: Device id.
        """
        output = Adb.run(command='shell pm uninstall ' + app_id, device_id=device_id)
        assert 'Success' in output, 'Failed to uninstall {0}. \n Log: \n {1}'.format(app_id, output)

    @staticmethod
    def monkey(apk_file, device_id):
        """
        Perform monkey testing.
        :param apk_file: Application under test.
        :param device_id: Device id.
        """
        Adb.__monkey_kill(device_id)
        app_id = Adb.__get_pacakge_id(apk_file)
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
