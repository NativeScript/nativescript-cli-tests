from distutils.cmd import Command
import os
import platform

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import UninstallCLI, InstallCLI, GetAndroidRuntime, GetiOSRuntime, \
    androidRuntimeSymlinkPath, iosRuntimeSymlinkPath, androidRuntimePath, \
    iosRuntimePath, GetModules, modulesPath
from helpers.device import StopEmulators
import tns_tests_runner


smokeTestResult = ""

def ExecuteTests():
    print "####RUNNING TESTS####"
    global smokeTestResult
    smokeTestResult = str(tns_tests_runner.RunTests())

def AnalyzeResultAndExit():
    global smokeTestResult
    if not ("errors=0" in smokeTestResult) or not ("failures=0" in smokeTestResult):
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':
   
    # Cleanup old runtimes
    
    CleanupFolder(os.path.split(androidRuntimeSymlinkPath)[0])
    CleanupFolder(os.path.split(iosRuntimeSymlinkPath)[0])
    CleanupFolder(modulesPath)
    if os.path.isfile(androidRuntimePath):
        os.remove(androidRuntimePath)
    if os.path.isfile(iosRuntimePath):
        os.remove(iosRuntimePath)
    if os.path.isfile(modulesPath):
        os.remove(modulesPath)
               
    # Cleanup folders created by test execution
    CleanupFolder('TNS App')
    CleanupFolder('TNS App')
    CleanupFolder('TNS_TempApp')
    CleanupFolder('folder')
    CleanupFolder('template')
                
    # Uninstall previous CLI and install latest   
    UninstallCLI()
    InstallCLI()
    
    # Get latest Android and iOS runtimes
    GetModules();
    GetAndroidRuntime()
    if 'Darwin' in platform.platform():
        GetiOSRuntime()
 
    # Clone hello-world template and update modules
    # TODO: Remove this code after v1 is released
    CleanupFolder('template-hello-world')
    runAUT("git clone git@github.com:NativeScript/template-hello-world.git template-hello-world")
    CleanupFolder("./template-hello-world/tns_modules")
    runAUT("mv " + os.path.join(os.path.splitext(modulesPath)[0],"package") + " tns_modules")
    runAUT("cp -R tns_modules template-hello-world")
           
    # Execute tests
    ExecuteTests()
    
    # Stop running emulators 
    if ('TESTRUN' in os.environ) and (not "SMOKE" in os.environ['TESTRUN']):       
        StopEmulators()
    
    # Exit        
    AnalyzeResultAndExit()