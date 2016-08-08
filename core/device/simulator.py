"""
Helper for working with simulator
"""

import time

from core.osutils.command import run
from core.osutils.process import Process
from core.settings.settings import SIMULATOR_NAME


class Simulator(object):
    @staticmethod
    def create(name, device_type, ios_version):
        """Create simulator"""

        print "~~~ Create simulator \"{0}\".".format(name)
        output = run(
                "xcrun simctl create \"{0}\" \"{1}\" \"{2}\"".format(name, device_type, ios_version))
        print "~~~ Simulator \"{0}\" created successfully.".format(name)
        print "~~~ Simulator \"{0}\" id: ".format(name) + output

    @staticmethod
    def start(name, sdk=None, timeout=300, wait_for=True):
        """Start iOS Simulator"""

        if sdk is not None:
            name = "{0} ({1})".format(name, sdk)
        print "~~~ Start simulator \"{0}\".".format(name)
        start_command = "instruments -w \"{0}\"".format(name)
        output = run(start_command, timeout)
        assert "Waiting for device to boot..." in output

        if wait_for:
            if Simulator.wait_for_simulator(timeout):
                print "~~~ Simulator \"{0}\" started successfully.".format(name)
            else:
                raise NameError("Waiting for simulator \"{0}\" failed!".format(name))

    @staticmethod
    def wait_for_simulator(timeout=300):
        """Wait for simulator"""

        found = False
        start_time = time.time()
        end_time = start_time + timeout
        while not found:
            time.sleep(2)
            output = run("xcrun simctl list devices")
            if "Booted" in output:
                found = True
                break
            if time.time() > end_time:
                break
        return found

    @staticmethod
    def stop_simulators():
        """Stop running simulators"""
        Process.kill("Simulator")
        time.sleep(1)

    @staticmethod
    def reset_simulators():
        """Reset settings and storage of all simulators"""
        Simulator.stop_simulators()
        run("xcrun simctl erase all", timeout=60)

    @staticmethod
    def delete(name):
        """Delete simulator"""

        output = run("xcrun simctl list | grep \"{0}\"".format(name))
        while (SIMULATOR_NAME in output) and ("Invalid" not in output):
            if "Booted" in output:
                run("xcrun simctl shutdown \"{0}\"".format(name))
                Simulator.stop_simulators()
            run("xcrun simctl delete \"{0}\"".format(name))
            print "~~~ Simulator \"{0}\" deleted.".format(name)
            output = run("xcrun simctl list | grep \"{0}\"".format(name))

    @staticmethod
    def get_id_by_name(name):
        """Get simulator id by name"""

        row_data = run("xcrun simctl list devices")
        row_list = row_data.split('\n')
        for row_line in row_list:
            if name in row_line and "Booted" in row_line:
                sim_id = Simulator.find_between(row_line, '(', ')')
                print "~~~ Booted simulator: " + row_line
                print "~~~ Booted simulator id: " + sim_id
                return sim_id

    @staticmethod
    def find_between(string, first, last):
        """Find string between two substrings"""

        try:
            start = string.index(first) + len(first)
            end = string.index(last, start)
            return string[start:end]
        except ValueError:
            return "ValueError!"

    @staticmethod
    def cat_app_file(app_name, file_path):
        """Return content of file on simulator"""
        print "~~~ Catenate ~~~"
        sim_id = Simulator.get_id_by_name(SIMULATOR_NAME)
        app_path = run("xcrun simctl get_app_container {0} org.nativescript.{1}".format(sim_id, app_name))
        print "~~~ Application path: " + app_path
        output = run("cat {0}/{1}".format(app_path, file_path))
        return output


    @staticmethod
    def file_contains(app_name, file_path, text):
        output = Simulator.cat_app_file(app_name, file_path)
        if text in output:
            print("{0} exists in {1}".format(text, file_path))
        else:
            print("{0} does not exists in {1}".format(text, file_path))
        assert text in output