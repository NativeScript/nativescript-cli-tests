import time

from time import sleep
from helpers._os_lib import runAUT


def RestartAdb():

    runAUT("adb kill-server")
    runAUT("adb start-server")
    runAUT("adb devices")


def StopApplication(appId, device_id):

    output = runAUT("adb -s " + device_id + " shell am force-stop " + appId)
    sleep(5)
    assert not (appId in output), "Failed to stop " + appId


def IsRunning(appId, device_id):

    output = runAUT("adb -s " + device_id + " shell ps | grep " + appId)
    if ("org.nativescript.TNSApp" in output):
        return True
    else:
        return False


def WaitUntilAppIsRunning(appId, device_id, timeout=60):

    isRunning = False
    endTime = time.time() + timeout
    while not isRunning:
        time.sleep(5)
        isRunning = IsRunning(appId, device_id)
        if (isRunning):
            break
        if (isRunning is False) and (time.time() > endTime):
            raise NameError(
                appId +
                " failed to start on " +
                device_id +
                " in " +
                timeout +
                " seconds.")
