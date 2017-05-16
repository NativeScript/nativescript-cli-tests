"""
Wrapper around libimobiledevice tools
"""
import os

from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File


class IDevice(object):

    @staticmethod
    def get_devices():
        """
        Get available iOS devices (only real devices).
        """
        device_ids = list()
        output = run(command='idevice_id --list', timeout=60, log_level=CommandLogLevel.SILENT)
        for line in output.splitlines():
            command = 'instruments -s | grep {0}'.format(line)
            check_connected = run(command=command, timeout=30, log_level=CommandLogLevel.SILENT)
            if 'null' not in check_connected:
                device_ids.append(line)
            else:
                message = '{0} is not trusted!'.format(line)
                print message
        return device_ids

    @staticmethod
    def get_screen(device_id, file_path):
        """
        Save screen of mobile device.
        :param device_id: Device identifier (example: `emulator-5554`).
        :param file_path: Name of image that will be saved.
        """

        base_path, file_name = os.path.split(file_path)
        file_name = file_name.rsplit('.', 1)[0]

        run(command="idevicescreenshot -u {0} {1}.tiff".format(device_id, file_name), log_level=CommandLogLevel.SILENT)
        run(command="sips -s format png {0}.tiff --out {1}".format(file_name, file_path),
            log_level=CommandLogLevel.SILENT)
        File.remove("{0}.tiff".format(file_name))

    @staticmethod
    def uninstall_all_app(device_id, app_prefix):
        """
        Uninstall all apps on all connected iOS physical devices.
        :param device_id: Device identifier.
        :param app_prefix: App prefix, for example: org.nativescript.
        """
        output = run("ideviceinstaller -u {0} -l".format(device_id), timeout=120)
        lines = output.splitlines()
        for line in lines:
            if app_prefix in line:
                app_name = line.split("-")[0]
                app_name = app_name.replace(" ", "")
                uninstall_result = run("ideviceinstaller -u {0} -U {1}".format(device_id, app_name), timeout=120)
                if "Uninstall: Complete" in uninstall_result:
                    print "{0} application successfully uninstalled.".format(app_prefix)
                else:
                    raise NameError("{0} application failed to uninstall.".format(app_prefix))
