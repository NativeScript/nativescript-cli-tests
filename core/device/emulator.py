"""
Helper for working with emulator
"""

import platform
import time

from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.process import Process
from core.settings.settings import TNS_PATH, CURRENT_OS, OSType, ADB_PATH, EMULATOR_PATH, EMULATOR_NAME, EMULATOR_PORT, \
    EMULATOR_ID


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
        print "Stop all emulators"
        Process.kill("emulator")
        Process.kill("emulator64-arm")
        Process.kill("emulator64-x86")
        Process.kill("emulator-arm")
        Process.kill("emulator-x86")
        Process.kill("qemu-system-arm")
        Process.kill("qemu-system-i386")
        Process.kill("qemu-system-i38")  # Linux

        output = run(ADB_PATH + " devices", log_level=CommandLogLevel.SILENT)  # Run `adb devices` for debug purposes.
        if "offline" in output:
            Emulator.restart_adb()

    @staticmethod
    def start_emulator(emulator_name, port="5554", timeout=300, wait_for=True):
        """Start Android Emulator
        :param emulator_name:
        :param port:
        :param timeout:
        :param wait_for:
        """
        print "Starting emulator on {0}".format(platform.platform())

        start_command = EMULATOR_PATH + " -avd " + emulator_name + " -port " + port + " -wipe-data"

        if CURRENT_OS == OSType.WINDOWS:
            run(start_command, timeout=10, output=False, wait=False)
        else:
            run(start_command + " &", timeout=timeout, output=False)

        if wait_for:
            # Check if emulator is running
            device_name = "emulator-" + port
            if Emulator.wait_for_device(device_name, timeout):
                print "Emulator started successfully."
            else:
                raise NameError("Wait for emulator failed!")

    @staticmethod
    def wait_for_device(device_name, timeout=600):
        """Wait for device
        :param device_name: Device name
        :param timeout:
        :return:
        """
        found = False
        start_time = time.time()
        end_time = start_time + timeout
        while not found:
            time.sleep(5)
            output = run(TNS_PATH + " device", log_level=CommandLogLevel.SILENT)
            if device_name in output:
                found = True
            if (found is True) or (time.time() > end_time):
                break

        return found

    @staticmethod
    def ensure_available():
        """Ensure Android Emulator is running"""
        output = run(TNS_PATH + " device android", log_level=CommandLogLevel.SILENT)
        lines = output.splitlines()
        found = False
        for line in lines:
            if ('emulator' in line) and ("Connected" in line):
                found = True
                break
        if found:
            time.slep(10)  # Adb returns device is available before it is booted. Wait a bit more...
            print "Emulator already running."
            # Make sure sdcard is not read-only
            run(ADB_PATH + " " + EMULATOR_ID + " shell mount -o rw,remount /system", log_level=CommandLogLevel.FULL)
            run(ADB_PATH + " " + EMULATOR_ID + " shell mount -o rw,remount rootfs /", log_level=CommandLogLevel.FULL)
            run(ADB_PATH + " " + EMULATOR_ID + " shell chmod 777 /mnt/sdcard", log_level=CommandLogLevel.FULL)

            # Set screen timeout
            run(ADB_PATH + " " + EMULATOR_ID + " shell rm -f /data/system/locksettings.db*",
                log_level=CommandLogLevel.FULL)
            print "Emulator configuration complete!"
        else:
            Emulator.stop_emulators()
            Emulator.start_emulator(emulator_name=EMULATOR_NAME, port=EMULATOR_PORT, wait_for=True)
        return found

    @staticmethod
    def cat_app_file(app_name, file_path):
        """Return content of file on emulator"""
        app_name = app_name.replace("_", "")
        app_name = app_name.replace(" ", "")
        output = run(ADB_PATH + " -s emulator-5554 shell run-as org.nativescript." +
                     app_name + " cat files/" + file_path)
        return output

    @staticmethod
    def file_contains(app_name, file_path, text):
        """Assert file on emulator contains text"""
        output = Emulator.cat_app_file(app_name, file_path)
        if text in output:
            print("{0} exists in {1}".format(text, file_path))
        else:
            print("{0} does not exists in {1}".format(text, file_path))
        assert text in output
