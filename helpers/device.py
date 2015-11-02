import os
import platform
import time

from helpers._os_lib import runAUT, KillProcess
from helpers._tns_lib import tnsPath
from helpers.adb import RestartAdb


def StartEmulator(emulatorName, port="5554", timeout=300, waitFor=True):

    print "Starting emulator on {0}".format(platform.platform())

    if ('ACTIVE_UI' in os.environ):
        if ("NO" in os.environ['ACTIVE_UI']):
            startCommand = "emulator -avd " + emulatorName + " -port " + port + " -no-skin -no-audio -no-window"
        else:
            startCommand = "emulator -avd " + emulatorName + " -port " + port

    if 'Windows' in platform.platform():
        runAUT(startCommand, timeout, False)
    else:
        runAUT(startCommand + " &", timeout, False)

    if (waitFor):
        # Check if emulator is running
        deviceName = "emulator-" + port
        if WaitForDevice(deviceName, timeout):
            print "Emulator started successfully."
        else:
            raise NameError("Wait for emulator failed!")

def WaitForDevice(deviceName, timeout=600):

    found = False
    startTime = time.time()
    endTime = startTime + timeout;
    while not found:
        time.sleep(5)
        output = runAUT(tnsPath + " device")
        if (deviceName in output):
            found = True
        if (time.time() > startTime + 60):
            RestartAdb()
        if (found is True) or (time.time() > endTime):
            break
    return found

def StopEmulators():
    KillProcess("emulator")
    KillProcess("emulator64-arm")
    KillProcess("emulator64-x86")

def StopSimulators():
    KillProcess("iOS Simulator")
    KillProcess("Simulator")

def GivenRunningEmulator():

    output = runAUT(tnsPath + " device")
    if not ('emulator' in output):
        output = runAUT(tnsPath + " device")
        if not ('emulator' in output):
            StopEmulators()
            StartEmulator(emulatorName="Api19", port="5554", waitFor=True)

def GivenRealDeviceRunning(platform):

    count = GetDeviceCount(platform, excludeEmulators=True)
    if (count > 0):
        print "{0} {1} devices are running".format(count, platform)
    else:
        raise NameError("No real android devices attached to this host.")

# Get Id of first connected physical device
def GetPhysicalDeviceId(platform):

    deviceId = None
    output = runAUT(tnsPath + " device " + platform)
    lines = output.splitlines()
    for line in lines:
        lline = line.lower()
        if (platform in lline) and (not ("emulator" in lline)):
            deviceId = lline.split((platform), 1)[1].replace(" ", "")  # deviceId = @030b206908e6c3c5@
            deviceId = deviceId[3:-3]  # devideId = 030b206908e6c3c5
            print deviceId
    return deviceId

# Get device count
def GetDeviceCount(platform="", excludeEmulators=False):

    output = runAUT(tnsPath + " device " + platform)
    lines = output.splitlines()
    count = len(lines)
    if (excludeEmulators):
        for line in lines:
            lline = line.lower()
            if ("emulator" in lline):
                count = count - 1
    return count;
