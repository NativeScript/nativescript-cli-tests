import os
import re
import time

from helpers._os_lib import runAUT, KillProcess

def CreateEmulator():

    emulatorCreated = False    
    for apiLevel in range (17, 20):
        command="echo no | android create avd -n TempDevice -t android-{0} -b x86 -f".format(apiLevel)
        output = runAUT(command)
        if ("Error" in output):
            print "Failed to create emulator with android-{0} target and x86 abi.".format(apiLevel)
            command = "echo no | android create avd -n TempDevice -t android-{0} -f".format(apiLevel)
            output = runAUT(command)
            if ("Error" in output):
                print "Failed to create emulator with android-{0} target and default abi.".format(apiLevel)
            else:
                print "Emulator with android-{0} target created successfully.".format(apiLevel)
                emulatorCreated = True 
                break;
        else:
            print "Emulator with android-{0} target created successfully.".format(apiLevel)
            emulatorCreated = True
            break;

    if (emulatorCreated):
        pass
    else:
        raise NameError("Failed to create emulator!")
    
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
