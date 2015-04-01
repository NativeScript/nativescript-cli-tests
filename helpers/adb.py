import time

from time import sleep
from helpers._os_lib import runAUT


def StopApplication(appId, deviceId):
    
    output = runAUT("adb -s " + deviceId + " shell am force-stop " + appId)
    sleep(5)
    assert not (appId in output), "Failed to stop " + appId

def IsRunning(appId, deviceId):
    
    output = runAUT("adb -s " + deviceId + " shell ps | " + appId)
    if ("org.nativescript.TNSApp" in output):
        return True
    else:
        return False 
    
def WaitUntilAppIsRunning(appId, deviceId, timeout=60):
    
    isRunning = False
    endTime = time.time() + timeout;
    while not isRunning:
        time.sleep(5)
        isRunning = IsRunning(appId, deviceId)
        if (isRunning):
            break 
        if (isRunning is False) and (time.time() > endTime):
            raise NameError(appId + " failed to start on " + deviceId + " in " + timeout + " seconds.")