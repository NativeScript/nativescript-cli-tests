'''
Helper for working with simulator
'''

import time

from helpers._os_lib import run_aut, kill_process

def start_simulator(name, timeout=300, wait_for=True):
    '''Start iOS Simulator'''

    print "Starting simulator \"{0}\".".format(name)
    start_command = "instruments -w \"{0}\"".format(name)
    output = run_aut(start_command, timeout)
    assert "Waiting for device to boot..." in output

    if wait_for:
        if wait_for_simulator(timeout):
            print "\"{0}\" simulator started successfully.".format(name)
        else:
            raise NameError("Wait for simulator \"{0}\" failed!".format(name))

def wait_for_simulator(timeout=300):
    '''Wait for simulator'''

    found = False
    start_time = time.time()
    end_time = start_time + timeout
    while not found:
        time.sleep(5)
        output = run_aut("xcrun simctl list")
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
