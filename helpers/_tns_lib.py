import os
import platform
import shutil
import time

from _os_lib import runAUT


tnsPath = os.path.join('node_modules', '.bin', 'tns');

def InstallCLI(pathToPackage=None):
    """
    """
    print os.environ
    if 'BUILD_CLI_PATH' in os.environ:
        location = os.path.join(os.environ['BUILD_CLI_PATH'], "nativescript.tgz")
        shutil.copy2(location.strip(), (os.path.join(os.getcwd(), "nativescript.tgz")))
    if pathToPackage != None:
        shutil.copy2(pathToPackage, (os.path.join(os.getcwd(), "nativescript.tgz")))

    installCommand = "npm i nativescript.tgz"
    output = runAUT(installCommand)
    print output
    
    # TODO: Remove this check after https://github.com/NativeScript/nativescript-cli/issues/113 is fixed
    if "Linux" in platform.platform():
        addExecute = "chmod u+x node_modules/nativescript/resources/platform-tools/android/linux/adb"
        output = runAUT(addExecute)
        print output

def UninstallCLI():    
    uninstallCommand = "npm rm nativescript"
    output = runAUT(uninstallCommand)
    print output

def CreateProject(projName, path=None, appId=None, copyFrom=None):
    shutil.rmtree(projName, True)  # make sure no old project exists
    time.sleep(1)  # to be sure that shutil has finished
    
    command = tnsPath + " create {0}".format(projName)
    
    if path != None:
        command += " --path " + path;
    if appId != None:
        command += " --appid " + path;
    if copyFrom != None:
        command += " --copy-from " + path;

    outp = runAUT(command)
    assert("{0} was successfully created".format(projName) in outp)

def GetCLIBuildVersion():
    command = tnsPath + " --version"
    outp = runAUT(command)
    return outp