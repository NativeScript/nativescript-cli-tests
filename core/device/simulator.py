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
    def __get_id(name):
        """
        Find simulator GUID by Simulator name
        :param name: Simulator name
        :return: Simulator GUID
        """
        output = run(command='xcrun simctl list | grep \'{0}\''.format(name), log_level=CommandLogLevel.SILENT)
        lines = output.splitlines()
        if len(lines) > 1:
            raise AssertionError("Multiple simulators with same name found!")
        elif len(lines) == 0:
            return None
        else:
            return lines[0].split('(')[1].split(')')[0]

    @staticmethod
    def __get_state(simulator_id):
        """
        Find state of Simulator by id
        :param simulator_id: Simulator GUID
        :return: State as string
        """
        output = run(command='xcrun simctl list | grep {0}'.format(simulator_id), log_level=CommandLogLevel.SILENT)
        lines = output.splitlines()
        if len(lines) == 0:
            raise AssertionError("Can not find device with id " + simulator_id)
        else:
            return lines[0].split('(')[-1].split(')')[0]

    @staticmethod
    def create(name, device_type, ios_version):
        """
        Create iOS Simulator.
        :param name: Simulator name.
        :param device_type: Device type, example: 'iPhone 7'
        :param ios_version: iOS Version, example: '10.0'
        """

        # Ensure simulators are stopped
        Simulator.stop()
        Simulator.delete(SIMULATOR_NAME)

        ios_version = ios_version.replace('.', '-')
        sdk = "com.apple.CoreSimulator.SimRuntime.iOS-{0}".format(ios_version)
        create_command = 'xcrun simctl create "{0}" "{1}" "{2}"'.format(name, device_type, sdk)
        output = run(command=create_command, log_level=CommandLogLevel.SILENT)
        assert 'Invalid' not in output, 'Failed to create simulator. \n ' + output
        assert 'error' not in output.lower(), 'Failed to create simulator. \n ' + output
        assert '-' in output, 'Failed to create simulator. Output is not GUID. \n' + output
        print 'iOS Simulator created: ' + name

    @staticmethod
    def start(name, timeout=300):
        """
        Start iOS Simulator
        :param name: Simulator name.
        :param sdk: iOS Version, example '10.0'
        :param timeout: Timeout in seconds.
        :return: Identifier of booted iOS Simulator.
        """

        # Find simulator GUID
        sim_id = Simulator.__get_id(name)
        if sim_id is None:
            raise AssertionError("Unable to find device with name " + name)

        # Fire start command
        start_command = 'xcrun simctl boot {0}'.format(sim_id)
        output = run(command=start_command, timeout=timeout, log_level=CommandLogLevel.SILENT)
        assert 'Invalid device' not in output, "Can not find simulator with id " + sim_id
        assert 'Unable to boot' not in output, "Failed to boot " + sim_id
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
        Check if simulator with given name is running
        :param simulator_name: Simulator name
        :return: Boolean value for simulator state and string with simulator id (if it is running).
        """
        running = False
        if simulator_name == None:
            output = run(command='xcrun simctl list devices | grep Boot', timeout=60, log_level=CommandLogLevel.SILENT)
            lines = output.splitlines()
            if len(lines) > 0:
                if Process.is_running(proc_name="Simulator"):
                    running = True
                    simid = lines[0].split('(')[1].split(')')[0]
                else:
                    print "Simulator report to be booted, but Simulator process is not running!"
            else:
                simid = None
        else:
            simid = Simulator.__get_id(name=simulator_name)
            if Simulator.__get_state(simulator_id=simid) == 'Booted':
                running = True
        return running, simid

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
    def stop(device_id='booted'):
        """
        Stop running simulators (by default stop all simulators)
        :param device_id: Device identifier (Simulator GUID)
        """
        Process.kill('Simulator')
        time.sleep(1)
        if device_id == 'booted':
            print 'Stop all running simulators.'
        else:
            print 'Stop simulator with id ' + device_id
        run(command='xcrun simctl shutdown {0}'.format(device_id), timeout=60, log_level=CommandLogLevel.SILENT)
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
    def get_screen(device_id, file_path):
        """
        Save screen of iOS Simulator.
        :param device_id: Device identifier (Simualtor GUID)
        :param file_path: Name of image that will be saved.
        """
        run(command="xcrun simctl io {0} screenshot {1}".format(device_id, file_path), log_level=CommandLogLevel.SILENT)
