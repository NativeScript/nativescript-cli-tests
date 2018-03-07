"""
Helper for working with emulator
"""
import os
import time

from core.device.device import Device
from core.device.helpers.adb import Adb
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.osutils.process import Process
from core.settings.settings import EMULATOR_NAME, EMULATOR_PORT, EMULATOR_ID, CURRENT_OS

EMULATOR_PATH = os.path.join(os.environ.get('ANDROID_HOME'), 'tools', 'emulator')


class Emulator(object):
    @staticmethod
    def stop():
        """
        Stop all running emulators.
        """
        print 'Stop all running emulators.'

        Process.kill_by_commandline('qemu')
        Process.kill_by_commandline('emulator64')

        Process.kill('emulator64-arm')
        Process.kill('emulator64-x86')
        Process.kill('emulator-arm')
        Process.kill('emulator-x86')
        Process.kill('qemu-system-arm')
        Process.kill('qemu-system-i386')
        Process.kill('qemu-system-i38')

        assert not Emulator.is_running(device_id=EMULATOR_ID), 'Emulator is still running!'

    @staticmethod
    def start(emulator_name=EMULATOR_NAME, port=EMULATOR_PORT, timeout=300, wipe_data=True):
        """
        Start emulator.
        :param wipe_data: If true it will wipe emulator date.
        :param emulator_name: Name of android emulator image (avd).
        :param port: Port for Android emulator.
        :param timeout: Time to wait until emulator boot.
        """
        print 'Starting emulator {0}'.format(emulator_name)
        start_command = EMULATOR_PATH + ' -avd ' + emulator_name + ' -port ' + port
        if wipe_data:
            start_command = start_command + ' -wipe-data'
        log_file = run(start_command, timeout=timeout, wait=False, log_level=CommandLogLevel.COMMAND_ONLY)

        # Check if emulator is running
        device_name = 'emulator-' + port
        if Emulator.wait(device_name, timeout):
            print 'Emulator started successfully.'
        else:
            print 'Emulator failed to boot!'
            print File.read(log_file)
            raise Exception('Wait for emulator failed!')

    @staticmethod
    def is_running(device_id):
        """
        Check if device is is currently available.
        :param device_id: Device id.
        :return: True if running, False if not running.
        """
        if CURRENT_OS == OSType.WINDOWS:
            command = "shell dumpsys window windows | findstr mFocusedApp"
        else:
            command = "shell dumpsys window windows | grep -E 'mFocusedApp'"
        output = Adb.run(command=command, device_id=device_id, log_level=CommandLogLevel.SILENT)
        if 'ActivityRecord' in output:
            return True
        else:
            return False

    @staticmethod
    def wait(device_id, timeout=300):
        """
        Wait until emulator is up and running.
        :param device_id: Device name
        :param timeout: Timeout until device is ready (in seconds).
        :return: True if device is ready before timeout, otherwise - False.
        """
        booted = False
        start_time = time.time()
        end_time = start_time + timeout
        while not booted:
            time.sleep(5)
            booted = Emulator.is_running(device_id=device_id)
            if (booted is True) or (time.time() > end_time):
                break

        # If booted, make sure screen will not lock
        if booted:
            Adb.run(command='shell settings put system screen_off_timeout -1', device_id=device_id)

        # If booted, make sure screen will not lock
        if booted:
            text = Adb.get_page_source(device_id=device_id)
            if "android.process.acore" in text:
                print "Error dialog detected! Try to kill it..."
                Device.click(device_id=device_id, text="OK", timeout=10)
        return booted

    @staticmethod
    def ensure_available(emulator_name=EMULATOR_NAME):
        """
        Ensure Android Emulator is running.
        """
        found = Emulator.is_running(device_id=EMULATOR_ID)
        if found:
            print 'Emulator already running, reboot it...'
            Adb.run(command="shell rm -rf /data/local/tmp/*", device_id=EMULATOR_ID, log_level=CommandLogLevel.FULL)
            Adb.uninstall_all_apps(device_id=EMULATOR_ID)
            Adb.run(command="reboot", device_id=EMULATOR_ID, log_level=CommandLogLevel.FULL)
            Emulator.wait(device_id=EMULATOR_ID)
        else:
            Emulator.stop()
            Emulator.start(emulator_name=emulator_name, port=EMULATOR_PORT)
        return found
