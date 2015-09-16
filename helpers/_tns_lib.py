import os
import platform
import shutil

from helpers._os_lib import runAUT, FileExists, ExtractArchive
from time import sleep


tnsPath = os.path.join('node_modules', '.bin', 'tns');
nativescriptPath = os.path.join('node_modules', '.bin', 'nativescript');
androidRuntimePath = "tns-android.tgz"
iosRuntimePath = "tns-ios.tgz"
androidRuntimeSymlinkPath = os.path.join('tns-android', 'package')
iosRuntimeSymlinkPath = os.path.join('tns-ios', 'package')

androidKeyStorePath = os.environ.get('androidKeyStorePath')
androidKeyStorePassword = os.environ.get('androidKeyStorePassword')
androidKeyStoreAlias = os.environ.get('androidKeyStoreAlias')
androidKeyStoreAliasPassword = os.environ.get('androidKeyStoreAliasPassword')

if 'Darwin' in platform.platform():
    keychain = os.environ.get('KEYCHAIN')
    keychainPass = os.environ.get('KEYCHAIN_PASS', '')

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
        
        currentDir = os.getcwd()   
        os.chdir(os.path.join(currentDir, iosRuntimeSymlinkPath))    
        runAUT("npm install")
        os.chdir(currentDir);
        
                               
def UninstallCLI():        
    uninstallCommand = "npm rm nativescript"
    output = runAUT(uninstallCommand)
    print output

def CreateProject(projName, path=None, appId=None, copyFrom=None):

    # If --copy-from is not specified explicitly then project will copy template-hello-world
    if copyFrom == None:
        copyFrom = "template-hello-world"

    command = tnsPath + " create {0}".format(projName)

    if path != None:
        command += " --path " + path
    if appId != None:
        command += " --appid " + appId
    if copyFrom != None:
        command += " --copy-from " + copyFrom

    output = runAUT(command)
    assert ("Project {0} was successfully created".format(projName.replace("\"", "")) in output)
    return output

def PlatformAdd(platform=None, frameworkPath=None, path=None, symlink=False, assertSuccess=True):

    command = tnsPath + " platform add"

    if platform is not None:
        command += " {0}".format(platform)

    if frameworkPath is not None:
        command += " --frameworkPath {0}".format(frameworkPath)

    if path is not None:
        command += " --path {0}".format(path)

    if symlink is True:
        command += " --symlink"

    output = runAUT(command)

    if assertSuccess:
        assert ("Copying template files..." in output)
        assert ("Project successfully created" in output)

    return output

def Prepare(path=None, platform=None, logTrace=False, assertSuccess=True):

    command = tnsPath + " prepare"

    if platform is not None:
        command += " {0}".format(platform)

    if path is not None:
        command += " --path {0}".format(path)

    if logTrace:
        command += " --log trace"

    output = runAUT(command)

    if assertSuccess:
        assert ("Project successfully prepared" in output)

    return output

def LibraryAdd(platform=None, libPath=None, path=None, assertSuccess=True):

    command = tnsPath + " library add"

    if platform is not None:
        command += " {0}".format(platform)

    if libPath is not None:
        command += " {0}".format(libPath)

    if path is not None:
        command += " --path {0}".format(path)

    output = runAUT(command)

    if assertSuccess:
        if platform is "android":
            assert ("was successfully added for android platform" in output)
        else:
            assert ("The iOS Deployment Target is now 8.0 in order to support Cocoa Touch Frameworks." in output)
            
    return output

def Build(platform=None, mode=None, path=None, logTrace=False, assertSuccess=True):

    command = tnsPath + " build"

    if platform is not None:
        command += " {0}".format(platform)

    if mode is not None:
        command += " --{0}".format(platform)

    if path is not None:
        command += " --path {0}".format(path)

    if logTrace:
        command += " --log trace"

    output = runAUT(command)

    if assertSuccess:
        assert ("Project successfully prepared" in output)
        if platform is "android":
            assert ("BUILD SUCCESSFUL" in output)
        else:
            assert ("BUILD SUCCEEDED" in output)
        assert ("Project successfully built" in output)
        assert not ("ERROR" in output)

    return output

def Run(platform=None, emulator=False, device=None, path=None, justLaunch=True, assertSuccess=True):

    command = tnsPath + " run"

    if platform is not None:
        command += " {0}".format(platform)

    if emulator:
        command += " --emulator"

    if device is not None:
        command += " --device {0}".format(device)

    if path is not None:
        command += " --path {0}".format(path)

    if justLaunch:
        command += " --justlaunch"

    output = runAUT(command)

    if assertSuccess:
        assert ("Project successfully prepared" in output)
        assert ("Project successfully built" in output)
        if platform is "android":
            assert ("Successfully deployed on device with identifier" in output)
        else:
            if emulator:
                assert ("Session started without errors." in output)
            else:
                assert ("Successfully deployed on device" in output)
                assert ("Successfully run application org.nativescript." in output)

    return output

def LiveSync(platform=None, emulator=False, device=None, watch=False, path=None, assertSuccess=True):

    command = tnsPath + " livesync"

    if platform is not None:
        command += " {0}".format(platform)

    if emulator:
        command += " --emulator"

    if device is not None:
        command += " --device {0}".format(device)

    if watch:
        command += " --watch"

    if path is not None:
        command += " --path {0}".format(path)

    output = runAUT(command + " --log trace")

    if assertSuccess:
        assert ("Project successfully prepared" in output)
        if platform is "android":
            assert ("Transferring project files..." in output)
            assert ("Successfully transferred all project files." in output)
            assert ("Applying changes..." in output)
            assert ("Successfully synced application org.nativescript." in output)
            sleep(10)
            
    return output

def CreateProjectAndAddPlatform(projName, platform=None, frameworkPath=None, symlink=False): 
    CreateProject(projName)
    PlatformAdd(platform, frameworkPath, projName, symlink)

def GetCLIBuildVersion():
    return runAUT(tnsPath + " --version")