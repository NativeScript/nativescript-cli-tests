import time, shutil
from _os_lib import *

def CreateProject(projName, path=None, appId=None, copyFrom=None):
    shutil.rmtree(projName, True)  # make sure no old project exists
    time.sleep(1)  # to be sure that shutil has finished
    
    command = "tns create {0}".format(projName)
    
    if path != None:
        command += " --path " + path;
    if appId != None:
        command += " --appid " + path;
    if copyFrom != None:
        command += " --copy-from " + path;

    outp = runAUT(command)
    assert("{0} was successfully created".format(projName) in outp)

def GetCLIBuildVersion():
    command = "tns --version"
    outp = runAUT(command)
    return outp
