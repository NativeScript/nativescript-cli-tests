'''
Helper for working with simulator
'''

# C0111 - Missing docstring
# pylint: disable=C0111

import time

from helpers._os_lib import run_aut, kill_process

def create_simulator(name, device_type, ios_version):
    '''Create simulator'''

    print "~~~ Create simulator \"{0}\".".format(name)
    output = run_aut(
        "xcrun simctl create \"{0}\" \"{1}\" \"{2}\"".format(name, device_type, ios_version))
    print "~~~ Simulator \"{0}\" created successfully.".format(name)
    print "~~~ Simulator \"{0}\" id: ".format(name) + output

def start_simulator(name, timeout=300, wait_for=True):
    '''Start iOS Simulator'''

    print "~~~ Start simulator \"{0}\".".format(name)
    start_command = "instruments -w \"{0}\"".format(name)
    output = run_aut(start_command, timeout)
    assert "Waiting for device to boot..." in output

    if wait_for:
        if wait_for_simulator(timeout):
            print "~~~ Simulator \"{0}\" started successfully.".format(name)
        else:
            raise NameError("Waiting for simulator \"{0}\" failed!".format(name))

def wait_for_simulator(timeout=300):
    '''Wait for simulator'''

    found = False
    start_time = time.time()
    end_time = start_time + timeout
    while not found:
        time.sleep(5)
        output = run_aut("xcrun simctl list devices")
        if "Booted" in output:
            found = True
            break
        if time.time() > end_time:
            break
    return found

def stop_simulators():
    '''Stop running simulators'''

    # Xcode6
    kill_process("iOS Simulator")
    # Xcode7
    kill_process("Simulator")

def delete_simulator(name):
    '''Delete simulator'''

    run_aut("xcrun simctl delete \"{0}\"".format(name))
    print "~~~ Simulator \"{0}\" deleted.".format(name)

def cat_app_file_on_simulator(app_name, file_path):
    '''Return content of file on simulator'''

    sim_id = get_simulator_id_by_name('iPhone 6s 90')
    app_path = run_aut(
        "xcrun simctl get_app_container {0} org.nativescript.{1}".format(sim_id, app_name))
    print "~~~ Application path: " + app_path
    output = run_aut("cat {0}/{1}".format(app_path, file_path))
    return output

def get_simulator_id_by_name(name):
    '''Get simulator id by name'''

    row_data = run_aut("xcrun simctl list devices")
    row_list = row_data.split('\n')
    for row_line in row_list:
        if name in row_line and "Booted" in row_line:
            sim_id = find_between(row_line, '(', ')')
            print "~~~ Booted simulator: " + row_line
            print "~~~ Booted simulator id: " + sim_id
            return sim_id

def find_between(string, first, last):
    '''Find string between two substrings'''

    try:
        start = string.index(first) + len(first)
        end = string.index(last, start)
        return string[start:end]
    except ValueError:
        return "ValueError!"
