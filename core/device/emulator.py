"""
Helper for working with emulator
"""

import os
import platform
import time

from core.osutils.command import run
from core.osutils.process import Process
from core.settings.settings import TNS_PATH, CURRENT_OS, OSType, ADB_PATH, EMULATOR_PATH


class Emulator(object):
    @staticmethod
    def restart_adb():
        """Restart Adb"""
        run(ADB_PATH + " kill-server")
        run(ADB_PATH + " start-server")
        run(ADB_PATH + " devices")

    @staticmethod
    def stop_emulators():
        """Stop running emulators"""
        Process.kill("emulator")
        Process.kill("emulator64-arm")
        Process.kill("emulator64-x86")
        Process.kill("quemu-system-i38")
        Process.kill("qemu-system-i386")

    @staticmethod
    def start_emulator(emulator_name, port="5554", timeout=300, wait_for=True):
        """Start Android Emulator"""
        print "Starting emulator on {0}".format(platform.platform())

        start_command = EMULATOR_PATH + " -avd " + emulator_name + " -port " + port
        if 'ACTIVE_UI' in os.environ:
            if "NO" in os.environ['ACTIVE_UI']:
                start_command = start_command + " -no-skin -no-audio -no-window"

        if CURRENT_OS == OSType.WINDOWS:
            run(start_command, timeout, False)
        else:
            run(start_command + " &", timeout, False)

        if wait_for:
            # Check if emulator is running
            device_name = "emulator-" + port
            if Emulator.wait_for_device(device_name, timeout):
                print "Emulator started successfully."
            else:
                raise NameError("Wait for emulator failed!")

    @staticmethod
    def wait_for_device(device_name, timeout=600):
        """Wait for device"""
        found = False
        start_time = time.time()
        end_time = start_time + timeout
        while not found:
            time.sleep(5)
            output = run(TNS_PATH + " device")
            if device_name in output:
                found = True
            if time.time() > start_time + 120:
                Emulator.restart_adb()
            if (found is True) or (time.time() > end_time):
                break

        return found

    @staticmethod
    def ensure_available():
        """Ensure Android Emulator is running"""
        output = run(TNS_PATH + " device")
        if 'emulator' not in output:
            output = run(TNS_PATH + " device")
            if not 'emulator' in output:
                Emulator.stop_emulators()
                Emulator.start_emulator(emulator_name="Api19", port="5554", wait_for=True)

    @staticmethod
    def cat_app_file(app_name, file_path):
        '''Return content of file on emulator'''
        print "~~~ Catenate ~~~"
        output = run(ADB_PATH + " -s emulator-5554 shell run-as org.nativescript." + \
                     app_name + " cat files/" + file_path)
        return output
