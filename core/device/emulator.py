"""
Helper for working with emulator
"""
import os
import time

from core.device.helpers.adb import Adb
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.process import Process
from core.settings.settings import EMULATOR_NAME, EMULATOR_PORT, EMULATOR_ID

EMULATOR_PATH = os.path.join(os.environ.get('ANDROID_HOME'), 'tools', 'emulator')


class Emulator(object):
    @staticmethod
    def stop():
        """
        Stop running emulators.
        """
        print 'Stop all emulators'
        Process.kill('emulator')
        Process.kill('emulator64-arm')
        Process.kill('emulator64-x86')
        Process.kill('emulator-arm')
        Process.kill('emulator-x86')
        Process.kill('qemu-system-arm')
        Process.kill('qemu-system-i386')
        Process.kill('qemu-system-i38')  # Linux

    @staticmethod
    def start(emulator_name=EMULATOR_NAME, port=EMULATOR_PORT, timeout=300):
        """
        Start emulator.
        :param emulator_name: Name of android emulator image (avd).
        :param port: Port for Android emulator.
        :param timeout: Time to wait until emulator boot.
        """
        print 'Starting emulator {0}'.format(emulator_name)
        start_command = EMULATOR_PATH + ' -avd ' + emulator_name + ' -port ' + port + ' -wipe-data'
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

        return booted

    @staticmethod
    def ensure_available():
        """
        Ensure Android Emulator is running.
        """
        found = Emulator.is_running(device_id=EMULATOR_ID)
        if found:
            print 'Emulator already running.'
        else:
            Emulator.stop()
            Emulator.start(emulator_name=EMULATOR_NAME, port=EMULATOR_PORT)
        return found
