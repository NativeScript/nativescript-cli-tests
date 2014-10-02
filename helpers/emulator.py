import os
import re
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
    
    print "Starting emulator on {0} OS".format(os.name) 
    StopEmulators()    
    startCommand = "emulator -avd TempDevice -no-skin -no-audio -no-window"     
   
    # Start emulator
    if 'nt' in os.name:
        runAUT(startCommand, None, False)
    else:                      
        runAUT(startCommand + " &", None, False)

    # Retry to start emulator if it is not running
    if WaitForEmulator():
        print "Emulator is started successfully."
        pass
    else:
        KillProcess("adb")
        StopEmulators()
        if 'nt' in os.name:
            runAUT(startCommand, None, False)
        else:                      
            runAUT(startCommand + " &", None, False)
    
        # Raise error if emulator is still not running                  
        if WaitForEmulator():
            print "Emulator is started successfully."
        else:
            raise NameError("Wait for emulator failed!")

def WaitForEmulator():
    result = False
    for counter in range(1, 10):
        time.sleep(5)
        output = runAUT("adb devices");
        if "emulator-5554device" in re.sub(re.compile(r'\s+'), '', output):
            result = True 
            break 
    return result;
                   
def StopEmulators():
    KillProcess("emulator")
