import os
import platform
import time

from helpers._os_lib import run_aut, kill_process
from helpers._tns_lib import tnsPath
from helpers.adb import restart_adb

def start_emulator(emulatorName, port="5554", timeout=300, waitFor=True):

    print "Starting emulator on {0}".format(platform.platform())

    if ('ACTIVE_UI' in os.environ):
        if ("NO" in os.environ['ACTIVE_UI']):
            startCommand = "emulator -avd " + emulatorName + \
                " -port " + port + " -no-skin -no-audio -no-window"
        else:
            startCommand = "emulator -avd " + emulatorName + " -port " + port

    if 'Windows' in platform.platform():
        run_aut(startCommand, timeout, False)
    else:
        run_aut(startCommand + " &", timeout, False)

    if (waitFor):
        # Check if emulator is running
        deviceName = "emulator-" + port
        if wait_for_device(deviceName, timeout):
            print "Emulator started successfully."
        else:
            raise NameError("Wait for emulator failed!")


def wait_for_device(deviceName, timeout=600):

    found = False
    startTime = time.time()
    endTime = startTime + timeout
    while not found:
        time.sleep(5)
        output = run_aut(tnsPath + " device")
        if (deviceName in output):
            found = True
        if (time.time() > startTime + 60):
            restart_adb()
        if (found is True) or (time.time() > endTime):
            break
    return found


def stop_emulators():
    kill_process("emulator")
    kill_process("emulator64-arm")
    kill_process("emulator64-x86")


def stop_simulators():
    kill_process("iOS Simulator")
    kill_process("Simulator")


def given_running_emulator():

    output = run_aut(tnsPath + " device")
    if not ('emulator' in output):
        output = run_aut(tnsPath + " device")
        if not ('emulator' in output):
            stop_emulators()
            start_emulator(emulatorName="Api19", port="5554", waitFor=True)


def given_real_device(platform):

    count = get_device_count(platform, excludeEmulators=True)
    if (count > 0):
        print "{0} {1} devices are running".format(count, platform)
    else:
        raise NameError("No real android devices attached to this host.")

# Get Id of first connected physical device


def get_physical_device_id(platform):

    deviceId = None
    output = run_aut(tnsPath + " device " + platform)
    lines = output.splitlines()
    for line in lines:
        lline = line.lower()
        if (platform in lline) and (not ("emulator" in lline)):
            deviceId = lline.split(
                (platform), 1)[1].replace(
                " ", "")  # deviceId = @030b206908e6c3c5@
            deviceId = deviceId[3:-3]  # devideId = 030b206908e6c3c5
            print deviceId
    return deviceId

# Get device count


def get_device_count(platform="", excludeEmulators=False):

    output = run_aut(tnsPath + " device " + platform)
    lines = output.splitlines()
    count = len(lines)
    if (excludeEmulators):
        for line in lines:
            lline = line.lower()
            if ("emulator" in lline):
                count = count - 1
    return count
