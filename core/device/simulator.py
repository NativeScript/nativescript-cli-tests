"""
Helper for working with simulator
"""

import time

from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.process import Process
from core.settings.settings import SIMULATOR_NAME


class Simulator(object):
    @staticmethod
    def create(name, device_type, ios_version):
        """
        Create iOS Simulator.
        :param name: Simulator name.
        :param device_type: Device type, example: 'iPhone 7'
        :param ios_version: iOS Version, example: '10.0'
        """
        ios_version = ios_version.replace('.', '-')
        sdk = "com.apple.CoreSimulator.SimRuntime.iOS-{0}".format(ios_version)
        create_command = 'xcrun simctl create "{0}" "{1}" "{2}"'.format(name, device_type, sdk)
        output = run(command=create_command, log_level=CommandLogLevel.SILENT)
        assert 'Invalid' not in output, 'Failed to create simulator. \n ' + output
        assert 'error' not in output.lower(), 'Failed to create simulator. \n ' + output
        assert '-' in output, 'Failed to create simulator. Output is not GUID. \n' + output
        print 'iOS Simulator created: ' + name

    @staticmethod
    def start(name, sdk=None, timeout=300):
        """
        Start iOS Simulator
        :param name: Simulator name.
        :param sdk: iOS Version, example '10.0'
        :param timeout: Timeout in seconds.
        :return: Identifier of booted iOS Simulator.
        """

        # Generate simulator name based on version
        if sdk is not None:
            name = '{0} ({1})'.format(name, sdk)

        # Fire start command
        start_command = 'instruments -w "{0}"'.format(name)
        output = run(command=start_command, timeout=timeout, log_level=CommandLogLevel.SILENT)
        assert 'Unknown device' not in output, "Can not find simulator with name " + name
        assert 'Waiting for device to boot...' in output
        print 'Simulator {0} is booting now...'.format(name)

        # Wait until simulator boot
        found, simulator_id = Simulator.wait_for_simulator(simulator_name=name, timeout=timeout)
        if found:
            print 'Simulator {0} with id {1} is up and running!'.format(name, simulator_id)
            return simulator_id
        else:
            raise NameError('Failed to boot {0}!'.format(name))

    @staticmethod
    def is_running(simulator_name=None):
        """

        :param simulator_name:
        :return:
        """
        running = False
        simulator_id = None
        output = run(command='xcrun simctl list devices', log_level=CommandLogLevel.SILENT)
        if 'Booted' in output:
            for line in output.splitlines():
                # Line looks like this: 'iPhone7N (A63FC6CE-7954-438A-905D-8C03438AC3FD) (Booted)'
                if simulator_name is None:
                    if 'Booted' in line:
                        running = True
                        simulator_id = line.split('(')[1].split(')')[0]
                else:
                    if ('Booted' in line) and (simulator_name in line):
                        running = True
                        simulator_id = line.split('(')[1].split(')')[0]
            return running, simulator_id
        else:
            return False, None

    @staticmethod
    def wait_for_simulator(simulator_name=None, timeout=300):
        """
        Wait until simulator boot.
        :param simulator_name:
        :return:
        :param timeout: Timeout in seconds.
        :return: True if booted, False if it fails to boot.
        :return: Identifier of booted simulator (None if simulator fails to boot).
        """
        found = False
        simulator_id = None
        start_time = time.time()
        end_time = start_time + timeout
        while not found:
            found, simulator_id = Simulator.is_running(simulator_name=simulator_name)
            if time.time() > end_time or found:
                break
            time.sleep(5)
        return found, simulator_id

    @staticmethod
    def ensure_available(simulator_name=None):
        """
        Ensure iOS Simulator is running.
        :param simulator_name: iOS Simulator name.
        :return: True if booted, False if it fails to boot.
        :return: Identifier of booted simulator (None if simulator fails to boot).
        """
        found, simulator_id = Simulator.is_running(simulator_name=simulator_name)
        if found:
            print 'iOS Simulator is running.'
        else:
            Simulator.stop()
            simulator_id = Simulator.start(name=simulator_name, timeout=300)
        return simulator_id

    @staticmethod
    def stop():
        """
        Stop all running simulators.
        """
        Process.kill('Simulator')
        time.sleep(1)

    @staticmethod
    def reset():
        """
        Reset settings and storage of all simulators.
        """
        Simulator.stop()
        run(command='xcrun simctl erase all', timeout=60, log_level=CommandLogLevel.SILENT)
        print 'Reset settings and storage of all simulators.'

    @staticmethod
    def delete(name):
        """
        Delete simulator.
        :param name: Simulator name.
        """
        delete_output = ""
        output = run(command='xcrun simctl list | grep \'{0}\''.format(name), log_level=CommandLogLevel.SILENT)
        while (SIMULATOR_NAME in output) and ('Invalid' not in output):
            if 'Booted' in output:
                run('xcrun simctl shutdown \'{0}\''.format(name), log_level=CommandLogLevel.SILENT)
                Simulator.stop()
            delete_output = run('xcrun simctl delete \'{0}\''.format(name), log_level=CommandLogLevel.SILENT)
            output = run('xcrun simctl list | grep \'{0}\''.format(name), log_level=CommandLogLevel.SILENT)
        assert "Unable to delete" not in delete_output, "Failed to delete simulator {0}".format(name)
        print 'Simulator \'{0}\' deleted.'.format(name)

    @staticmethod
    def __get_bundle_path(package_id):
        """
        Get path of application deployed on Simulator
        :param package_id: Application (bundle) identifier.
        :return: Path to package deployed inside simulator.
        """
        command = 'xcrun simctl get_app_container booted {0}'.format(package_id)
        base_path = run(command=command, log_level=CommandLogLevel.SILENT)
        if 'No such file or directory' in base_path:
            raise NameError('Failed to get app container of {0}'.format(package_id))
        else:
            return base_path

    @staticmethod
    def __list_path(package_id, path):
        """
        List file of application.
        :param package_id: Package identifier.
        :param path: Path relative to root folder of the package.
        :return: List of files and folders
        """
        base_path = Simulator.__get_bundle_path(package_id=package_id)
        output = run(command='ls -la {0}/{1}'.format(base_path, path), log_level=CommandLogLevel.FULL)
        return output

    @staticmethod
    def path_exists(package_id, path, timeout=20):
        """
        Wait until path exists (relative based on folder where package is deployed) on iOS Simulator.
        :param package_id: Package identifier.
        :param path: Relative path (based on folder where pacakge is deployed).
        :param timeout: Timeout in seconds.
        :return: True if path exists, false if path does not exists
        """
        t_end = time.time() + timeout
        found = False
        while time.time() < t_end:
            files = Simulator.__list_path(package_id=package_id, path=path)
            if 'No such file or directory' not in files:
                found = True
                break
        return found

    @staticmethod
    def path_does_not_exist(package_id, path, timeout=20):
        """
        Wait until path does not exist (relative based on folder where package is deployed) on iOS Simulator.
        :param package_id: Package identifier.
        :param path: Relative path (based on folder where pacakge is deployed).
        :param timeout: Timeout in seconds.
        :return: True if path does not exist, false if path exists
        """
        t_end = time.time() + timeout
        found = True
        while time.time() < t_end:
            files = Simulator.__list_path(package_id=package_id, path=path)
            if 'No such file or directory' in files:
                found = False
                break
        return not found

    @staticmethod
    def stop_application(app_id):
        """
        Stop application
        :param app_id: Bundle identifier (example: org.nativescript.TestApp)
        """
        command = 'xcrun simctl terminate booted {0}'.format(app_id)
        run(command=command, log_level=CommandLogLevel.FULL)

    @staticmethod
    def get_screen(file_path):
        """
        Save screen of iOS Simulator.
        :param file_path: Name of image that will be saved.
        """
        run(command="xcrun simctl io booted screenshot {0}".format(file_path),log_level=CommandLogLevel.SILENT)
