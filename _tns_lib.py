import time, shutil
from _os_lib import *

tnsPath = os.path.join('node_modules', '.bin', 'tns');

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
