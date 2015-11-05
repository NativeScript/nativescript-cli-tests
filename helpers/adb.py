import time

from time import sleep
from helpers._os_lib import runAUT

def RestartAdb():

    runAUT("adb kill-server")
    runAUT("adb start-server")
    runAUT("adb devices")

def StopApplication(app_id, device_id):

    output = runAUT("adb -s " + device_id + " shell am force-stop " + app_id)
    sleep(5)
    assert not (app_id in output), "Failed to stop " + app_id


def IsRunning(app_id, device_id):

    output = runAUT("adb -s " + device_id + " shell ps | grep " + app_id)
    if ("org.nativescript.TNSApp" in output):
        return True
    else:
        return False


def WaitUntilAppIsRunning(app_id, device_id, timeout=60):

    isRunning = False
    endTime = time.time() + timeout
    while not isRunning:
        time.sleep(5)
        isRunning = IsRunning(app_id, device_id)
        if (isRunning):
            break
        if (isRunning is False) and (time.time() > endTime):
            raise NameError(app_id + " failed to start on " + device_id + " in " + timeout + " seconds.")
