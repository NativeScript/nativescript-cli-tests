import re
import time
import platform

from helpers._os_lib import runAUT, KillProcess

def StartEmulator(EmulatorName):
    
    print "Starting emulator on {0}".format(platform.platform()) 

    startCommand = "emulator -avd " + EmulatorName   
   
    # Linux and OSX test nodes has no active UI session.
    if 'Windows' in platform.platform():
        runAUT(startCommand, 300, False)
    else:          
        startCommand = startCommand  + " -no-skin -no-audio -no-window"            
        runAUT(startCommand + " &", 300, False)

    # Retry to start emulator if it is not running
    if WaitForEmulator():
        print "Emulator is started successfully."
        pass
    else:
        KillProcess("adb")
        StopEmulators()
        if 'Windows' in platform.platform():
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
    for counter in range(1, 30):
        time.sleep(5)
        output = runAUT("adb devices");
        if "emulator-5554device" in re.sub(re.compile(r'\s+'), '', output):
            result = True 
            break 
    return result;
                   
def StopEmulators():
    KillProcess("emulator")
    KillProcess("emulator64-arm")
    KillProcess("emulator64-x86")
