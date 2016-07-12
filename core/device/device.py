"""
Helper for working with real devices
"""
import os
import time

from core.osutils.command import run
from core.settings.settings import TNS_PATH

ADB_PATH = os.path.join(os.environ.get('ANDROID_HOME'), 'platform-tools', 'adb')


class Device(object):
    @staticmethod
    def ensure_available(platform):
        """Ensure real device is running"""
        count = Device.get_count(platform)
        if count > 0:
            print "{0} {1} devices are running".format(count, platform)
        else:
            raise TypeError("No real devices attached to this host.")

    @staticmethod
    def get_id(platform):
        """Get Id of first connected physical device"""
        list = Device.get_ids(platform)
        return list.pop(0)

    @staticmethod
    def get_ids(platform):
        """Get IDs of all connected physical devices"""
        device_ids = list()
        output = run(TNS_PATH + " device " + platform)
        lines = output.splitlines()
        for line in lines:
            if (platform.lower() in line.lower()) and (not "status" in line.lower()):
                device_id = line.split("\xe2\x94\x82")[4].replace(" ", "")
                print "{0} device with id {1} found.".format(platform, device_id)
                if "Emulator" not in line:
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
                output = run(ADB_PATH + " -s {0} shell pm list packages".format(device_id), timeout=120)
                lines = output.splitlines()
                for line in lines:
                    if app_prefix in line:
                        app_name = line.split(":")[1]
                        app_name = app_name.replace(" ","")
                        uninstall_result = run(ADB_PATH + " -s {0} shell pm uninstall {1}".format(device_id, app_name), timeout=120)
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
                        app_name = app_name.replace(" ","")
                        uninstall_result = run("ideviceinstaller -u {0} -U {1}".format(device_id, app_name), timeout=120)
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
        """Wait until app is running"""
        running = False
        end_time = time.time() + timeout
        while not running:
            time.sleep(5)
            running = Device.is_running(app_id, device_id)
            if running:
                break
            if (running is False) and (time.time() > end_time):
                raise NameError(app_id + " failed to start on " + device_id + " in " + str(timeout) + " seconds.")

    @staticmethod
    def cat_app_file(platform, app_name, file_path):
        '''Return content of file on device'''
        if platform is "android":
            device_id = Device.get_id(platform="android")
            command = ADB_PATH + " -s {0} shell run-as org.nativescript.{1} cat files/{2}"\
                .format(device_id, app_name, file_path)
        if platform is "ios":
            command = "ddb device get-file \"Library/Application Support/LiveSync/{0}\" --app org.nativescript.{1}"\
                .format(file_path, app_name)
        output = run(command)
        return output


    @staticmethod
    def file_contains(platform, app_name, file_path, text):
        output = Device.cat_app_file(platform, app_name, file_path)
        if text in output:
            print("{0} exists in {1}".format(text, file_path))
        else:
            print("{0} does not exists in {1}".format(text, file_path))
            print "----------------------------------------------------"
            print output
            print "----------------------------------------------------"
        assert text in output