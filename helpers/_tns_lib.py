import os
import platform
import shutil

from helpers._os_lib import runAUT, FileExists, ExtractArchive


tnsPath = os.path.join('node_modules', '.bin', 'tns');
nativescriptPath = os.path.join('node_modules', '.bin', 'nativescript');
androidRuntimePath = "tns-android.tgz"
iosRuntimePath = "tns-ios.tgz"
androidRuntimeSymlinkPath = os.path.join('tns-android', 'package')
iosRuntimeSymlinkPath = os.path.join('tns-ios', 'package')

androidKeyStorePath = os.environ['androidKeyStorePath']
androidKeyStorePassword = os.environ['androidKeyStorePassword']
androidKeyStoreAlias = os.environ['androidKeyStoreAlias']
androidKeyStoreAliasPassword = os.environ['androidKeyStoreAliasPassword']

if 'Darwin' in platform.platform():
    keychain = os.environ['KEYCHAIN']
    keychainPass = os.environ['KEYCHAIN_PASS']

def InstallCLI(pathToPackage=None):
    if 'CLI_PATH' in os.environ:
        location = os.path.join(os.environ['CLI_PATH'], "nativescript.tgz")
        shutil.copy2(location.strip(), (os.path.join(os.getcwd(), "nativescript.tgz")))
    if pathToPackage != None:
        shutil.copy2(pathToPackage, (os.path.join(os.getcwd(), "nativescript.tgz")))

    installCommand = "npm i nativescript.tgz"
    output = runAUT(installCommand)
    print output

def GetAndroidRuntime():    
    if 'ANDROID_PATH' in os.environ:
        location = os.path.join(os.environ['ANDROID_PATH'], androidRuntimePath)
        shutil.copy2(location.strip(), (os.path.join(os.getcwd(), androidRuntimePath)))
    if FileExists(os.path.join(os.getcwd(), androidRuntimePath)):
        ExtractArchive(androidRuntimePath, os.path.splitext(androidRuntimePath)[0])
    
def GetiOSRuntime():    
    if 'IOS_PATH' in os.environ:
        location = os.path.join(os.environ['IOS_PATH'], iosRuntimePath)
        shutil.copy2(location.strip(), (os.path.join(os.getcwd(), iosRuntimePath)))
    if FileExists(os.path.join(os.getcwd(), iosRuntimePath)):
        ExtractArchive(iosRuntimePath, os.path.splitext(iosRuntimePath)[0])
               
def UninstallCLI():        
    uninstallCommand = "npm rm nativescript"
    output = runAUT(uninstallCommand)
    print output

def CreateProject(projName, path=None, appId=None, copyFrom=None):
    
    # TODO: It looks we don't need this code. Delete if no problems found until next release
    #shutil.rmtree(projName, True)  # make sure no old project exists
    #time.sleep(1)  # to be sure that shutil has finished
    
    command = tnsPath + " create {0}".format(projName)
    
    if path != None:
        command += " --path " + path
    if appId != None:
        command += " --appid " + appId
    if copyFrom != None:
        command += " --copy-from " + copyFrom

    outp = runAUT(command)
    assert("{0} was successfully created".format(projName.replace("\"", "")) in outp)

def PlatformAdd(platform=None, frameworkPath=None, path=None, symlink=False):
 
    command = tnsPath + " platform add"
    
    if platform is not None:
        command += " {0}".format(platform)
        
    if frameworkPath is not None:
        command += " --frameworkPath {0}".format(frameworkPath)
        
    if path is not None:
        command += " --path {0}".format(path)
        
    if symlink is True:
        command += " --symlink"
        
    return runAUT(command)

def Prepare(path=None, platform=None, assertSuccess=True):
 
    command = tnsPath + " prepare"
    
    if platform is not None:
        command += " {0}".format(platform)
        
    if path is not None:
        command += " --path {0}".format(path)

    output = runAUT(command)
    
    if (assertSuccess):
        assert ("Project successfully prepared" in output)
    
    return output

def CreateProjectAndAddPlatform(projName, platform=None, frameworkPath=None, symlink=False): 
    CreateProject(projName)
    output = PlatformAdd(platform, frameworkPath, projName, symlink)
    assert("Copying template files..." in output)
    assert("Project successfully created" in output)

def GetCLIBuildVersion():
    return runAUT(tnsPath + " --version")