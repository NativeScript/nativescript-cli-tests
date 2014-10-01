import os
import time

from helpers._os_lib import KillProcess, runAUT


def StartEmulator(name="Nexus4"):
    
    KillProcess("emulator")
    
    print os.name
    
    #if 'nt' in os.name:
        #command = "emulator -avd {0}".format(name)
    #else:                      
        #command = "emulator -avd {0} &".format(name)
   
    #print "Execute: " + command        
    #os.system(command)
    
    runAUT("emulator -avd Nexus4 -no-skin -no-audio -no-window &", None, False)

def WaitForEmulator():

    for counter in range(1, 5):
        time.sleep(10)
        output = runAUT("adb devices");
        print output
        if "emulator-5554device" in output.replace(" ", ""):
            break

def StopEmulators():
    KillProcess("adb")
    KillProcess("emulator")
