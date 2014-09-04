import os, platform, shutil
from _os_lib import runAUT

def InstallCLI(pathToPackage=None):
    """
    """
    print os.environ
    if 'BUILD_CLI_PATH' in os.environ:
        location = os.path.join(os.environ['BUILD_CLI_PATH'], "nativescript.tgz")
        shutil.copy2(location.strip(), (os.path.join(os.getcwd(), "nativescript.tgz")))
    if pathToPackage != None:
        shutil.copy2(pathToPackage, (os.path.join(os.getcwd(), "nativescript.tgz")))

    installCommand = "npm i -g nativescript.tgz"
    output = runAUT(installCommand)
    print output

def UninstallCLI():
    uninstallCommand = "npm rm -g nativescript"
    output = runAUT(uninstallCommand)
    print output
