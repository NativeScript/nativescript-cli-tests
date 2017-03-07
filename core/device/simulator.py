'''
Helper for working with simulator
'''

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
        :param timeout: Timeout for starting simulator.
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
        if Simulator.wait_for_simulator(timeout):
            print 'Simulator {0} is up and running!'.format(name)
        else:
            raise NameError('Failed to boot {0}!'.format(name))

    @staticmethod
    def wait_for_simulator(timeout=300):
        """
        Wait until simulator boot.
        :param timeout: Timeout in seconds.
        :return: True if booted, False if it fails to boot.
        """
        found = False
        start_time = time.time()
        end_time = start_time + timeout
        while not found:
            output = run(command='xcrun simctl list devices', log_level=CommandLogLevel.SILENT)
            if 'Booted' in output:
                found = True
                break
            if time.time() > end_time:
                break
            time.sleep(5)
        return found

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
        output = run(command='xcrun simctl list | grep \'{0}\''.format(name), log_level=CommandLogLevel.SILENT)
        while (SIMULATOR_NAME in output) and ('Invalid' not in output):
            if 'Booted' in output:
                run('xcrun simctl shutdown \'{0}\''.format(name), log_level=CommandLogLevel.SILENT)
                Simulator.stop()
            output = run('xcrun simctl delete \'{0}\''.format(name), log_level=CommandLogLevel.SILENT)
            assert "Unable to delete" not in output, "Failed to delete simulator {0}".format(name)
            print 'Simulator \'{0}\' deleted.'.format(name)
            output = run('xcrun simctl list | grep \'{0}\''.format(name), log_level=CommandLogLevel.SILENT)

    @staticmethod
    def uninstall_app(app_name):
        app_name = app_name.replace('_', '')
        app_name = app_name.replace(' ', '')
        run('xcrun simctl uninstall booted org.nativescript.{0}'.format(app_name))

    @staticmethod
    def cat_app_file(app_name, file_path):
        app_name = app_name.replace('_', '')
        app_name = app_name.replace(' ', '')
        app_path = run('xcrun simctl get_app_container booted org.nativescript.{0}'.format(app_name))
        print 'Get content of: ' + app_path
        output = run('cat {0}/{1}'.format(app_path, file_path))
        return output

    @staticmethod
    def file_contains(app_name, file_path, text):
        output = Simulator.cat_app_file(app_name, file_path)
        if text in output:
            print('{0} exists in {1}'.format(text, file_path))
        else:
            print('{0} does not exists in {1}'.format(text, file_path))
        assert text in output
