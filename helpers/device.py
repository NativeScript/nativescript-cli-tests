# W0621 - Redefining name from outer scope
# pylint: disable=W0621
'''
Helper for working devices
'''
import os
import platform
import time

from helpers._os_lib import run_aut, kill_process
from helpers._tns_lib import TNS_PATH
from helpers.adb import restart_adb


EMULATOR_PATH = os.path.join(os.environ.get('ANDROID_HOME'), 'tools', 'emulator')

def start_emulator(emulator_name, port="5554", timeout=300, wait_for=True):
    '''Start Android Emulator'''

    print "Starting emulator on {0}".format(platform.platform())

    if 'ACTIVE_UI' in os.environ:
        if "NO" in os.environ['ACTIVE_UI']:
            start_command = EMULATOR_PATH + " -avd " + emulator_name + \
                " -port " + port + " -no-skin -no-audio -no-window"
        else:
            start_command = EMULATOR_PATH + " -avd " + emulator_name + " -port " + port

    if 'Windows' in platform.platform():
        run_aut(start_command, timeout, False)
    else:
        run_aut(start_command + " &", timeout, False)

    if wait_for:
        # Check if emulator is running
        device_name = "emulator-" + port
        if wait_for_device(device_name, timeout):
            print "Emulator started successfully."
        else:
            raise NameError("Wait for emulator failed!")

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

def wait_for_device(device_name, timeout=600):
    '''Wait for device'''

    found = False
    start_time = time.time()
    end_time = start_time + timeout
    while not found:
        time.sleep(5)
        output = run_aut(TNS_PATH + " device")
        if device_name in output:
            found = True
        if time.time() > start_time + 60:
            restart_adb()
        if (found is True) or (time.time() > end_time):
            break
    return found

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

def stop_emulators():
    '''Stop running emulators'''

    kill_process("emulator")
    kill_process("emulator64-arm")
    kill_process("emulator64-x86")

def stop_simulators():
    '''Stop running simulators'''

    # Xcode6
    kill_process("iOS Simulator")
    # Xcode7
    kill_process("Simulator")

def given_running_emulator():
    '''Ensure Android Emulator is running'''

    output = run_aut(TNS_PATH + " device")
    if not 'emulator' in output:
        output = run_aut(TNS_PATH + " device")
        if not 'emulator' in output:
            stop_emulators()
            start_emulator(emulator_name="Api19", port="5554", wait_for=True)

def given_real_device(platform):
    '''Ensure Android device is running'''

    count = get_device_count(platform, exclude_emulators=True)
    if count > 0:
        print "{0} {1} devices are running".format(count, platform)
    else:
        raise NameError("No real android devices attached to this host.")

def get_physical_device_id(platform):
    '''Get Id of first connected physical device'''

    device_id = None
    output = run_aut(TNS_PATH + " device " + platform)
    lines = output.splitlines()
    for line in lines:
        lline = line.lower()
        if (platform in lline) and (not "emulator" in lline):
            device_id = lline.split(
                (platform), 1)[1].replace(" ", "")  # deviceId = @030b206908e6c3c5@
            device_id = device_id[3:-3]  # devideId = 030b206908e6c3c5
            print device_id
    return device_id

def get_device_count(platform="", exclude_emulators=False):
    '''Get device count'''

    output = run_aut(TNS_PATH + " device " + platform)
    lines = output.splitlines()
    count = len(lines)
    if exclude_emulators:
        for line in lines:
            lline = line.lower()
            if "emulator" in lline:
                count = count - 1
    return count
