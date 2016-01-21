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
        count = Device.get_count(platform, exclude_emulators=True)
        if count > 0:
            print "{0} {1} devices are running".format(count, platform)
        else:
            raise TypeError("No real devices attached to this host.")

    @staticmethod
    def get_id(platform):
        """Get Id of first connected physical device"""
        device_id = None
        output = run(TNS_PATH + " device " + platform)
        lines = output.splitlines()
        for line in lines:
            lline = line.lower()
            if (platform in lline) and (not "emulator" in lline):
                device_id = lline.split(
                        (platform), 1)[1].replace(" ", "")  # deviceId = @030b206908e6c3c5@
                device_id = device_id[3:-3]  # devideId = 030b206908e6c3c5
                device_id = device_id.split("\xe2\x94\x82")[0]
                print device_id
        return device_id

    @staticmethod
    def get_count(platform="", exclude_emulators=False):
        """Get device count"""
        output = run(TNS_PATH + " device " + platform)
        lines = output.splitlines()
        count = len(lines)
        if exclude_emulators:
            for line in lines:
                lline = line.lower()
                if "emulator" in lline:
                    count = count - 1
        return count

    @staticmethod
    def uninstall_app(app_prefix, platform, fail=True):
        """Uninstall mobile app"""
        if platform == "android":
            output = run("ddb device uninstall org.nativescript." + app_prefix, timeout=120)
            if "[Uninstalling] Status: RemovingApplication" in output:
                print "{0} application successfully uninstalled.".format(app_prefix)
            else:
                if fail:
                    raise NameError(
                            "{0} application failed to uninstall.".format(app_prefix))
        else:
            output = run("ideviceinstaller -U " + app_prefix, timeout=120)
            if "Uninstall: Complete" in output:
                print "{0} application successfully uninstalled.".format(app_prefix)
            else:
                if fail:
                    raise NameError(
                            "{0} application failed to uninstall.".format(app_prefix))

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
        """Waint until app is running"""
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
        print "~~~ Catenate ~~~"
        if platform is "android":
            output = run(
                    ADB_PATH + " shell run-as org.nativescript." +
                    app_name +
                    " cat files/" +
                    file_path)
        if platform is "ios":
            output = run(
                    "ddb device get-file \"Library/Application Support/LiveSync/" +
                    file_path +
                    "\" --app org.nativescript." +
                    app_name)
        return output
