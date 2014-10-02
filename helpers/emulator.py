import os
import time

from helpers._os_lib import KillProcess, runAUT


def CreateEmulator():
    
    StopEmulators()
    output = runAUT("echo no | android create avd -n TempDevice -t android-17 -b x86 -f")
    if ("Error:" in output):        
        print "x86 abi is not available for 'android-17' target. Will create device with default abi."
        output = runAUT("echo no | android create avd -n TempDevice -t android-17 -f")
        if ("Error:" in output):
            raise NameError("Failed to create android with 'echo no | android create avd -n TempDevice -t android-17 -f' command. Plase make sure you have 'android-17' target.")    
    
def StartEmulator():
    
    StopEmulators()    
    print os.name    
    if 'nt' in os.name:
        runAUT("emulator -avd TempDevice -no-skin -no-audio -no-window", None, False)
    else:                      
        runAUT("emulator -avd TempDevice -no-skin -no-audio -no-window &", None, False)

def WaitForEmulator():

    for counter in range(1, 5):
        time.sleep(10)
        output = runAUT("adb devices");
        print output
        if "emulator-5554device" in output.replace(" ", ""):
            break

def StopEmulators():
    KillProcess("emulator")
