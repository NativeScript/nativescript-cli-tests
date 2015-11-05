import os
import errno
import fileinput
import time
import threading
import psutil
import shutil
import platform
import tarfile
from time import sleep


default_timeout = 180  # seconds
default_output_file = "output.txt"
DEBUG = 0


def runAUT(cmd, set_timeout=None, getOutput=True):
    def forkIt():
        # this function will be run in parallel thread
        # #    You can redirect the output to one place, and the errors to another.
        # #    dir file.xxx > output.msg 2> output.err
        # #    You can print the errors and standard output to a single file by using the "&1" command to redirect the output for STDERR to STDOUT and then sending the output from STDOUT to a file:
        # #    dir file.xxx 1> output.msg 2>&1

        print 'Thread started'
        if getOutput:
            os.system(cmd + ' 1> output.txt 2>&1')
        else:
            os.system(cmd)

    # prepare command line
    print "##### {0} Executing command : {1}".format(time.strftime("%X"), cmd)
    if os.path.exists(default_output_file):
        os.remove(default_output_file)
    thread = threading.Thread(target=forkIt)
    thread.start()
    # waiting for thread to finish or timeout
    if set_timeout is None:
        thread.join(default_timeout)
    else:
        thread.join(set_timeout)
    if thread.is_alive():
        print '#### Process has timeouted at ', time.strftime("%X")
        # kill node.js instance if tns has started it
        KillProcess("node", "tns")
        thread.join()
    # do get whenever exist in the pipe
    out = "NOT_COLLECTED"
    if getOutput:
        f = open(default_output_file, 'r')
        out = f.read()
        f.close()
    if DEBUG == 1:
        print out
        print 'Thread finished. Returning ', out

    try:
        print "##### OUTPUT BEGIN #####"
        print out
        print "##### OUTPUT END #####"
        return out.strip('\n\r')
    except:
        print "##### OUTPUT BEGIN #####"
        print "Failed to print output"
        print "##### OUTPUT END #####"


def CleanupFolder(folder):
    try:
        shutil.rmtree(folder, False)
        sleep(1)
    except:
        if (os.path.exists(folder)):
            if ('Windows' in platform.platform()):
                runAUT('rmdir /S /Q \"{}\"'.format(folder))
            else:
                runAUT('rm -rf ' + folder)
            sleep(1)

# Check if output of command contains string from file


def CheckOutput(output, fileName):
    f = open('testdata/outputs/' + fileName)
    expected_lines = 0
    for line in f:
        expected_lines += 1
        line = line.rstrip('\r\n')
        print "checking ", line
        if line not in output:
            print "Output does not contain: ", line
            return False
    return True

# Check if folder contains list of files


def CheckFilesExists(rootFolder, listFile, ignoreFileCount=True):
    f = open('testdata/files/' + listFile)
    expected_lines = 0
    for line in f:
        expected_lines += 1
        relPath = rootFolder + '/' + line.rstrip('\r\n')
        print "checking ", relPath
        if not os.path.exists(relPath):
            print "File " + relPath + " does not exist!"
            return False
    total = 0
    for root, dirs, files in os.walk(rootFolder):
        total += len(files)
        print files
    print "Total files : ", total
    print "Expected lines : ", expected_lines

    if ignoreFileCount:
        return True
    else:
        assert(expected_lines == total)

# Check if folder is empty


def IsEmpty(path):
    if os.listdir(path) == []:
        return True
    else:
        return False


def FolderExists(path):
    if os.path.isdir(path):
        return True
    else:
        return False


def FileExists(path):
    if os.path.exists(path):
        return True
    else:
        return False


def IsRunningProcess(processName):
    result = False
    for proc in psutil.process_iter():
        if processName in str(proc):
            result = True
    return result


def KillProcess(processName, commandLine=None):
    result = False
    for proc in psutil.process_iter():
        if processName in str(proc):
            if commandLine is None:
                proc.kill()
                print "Process : {0} has been killed".format(processName)
                result = True
            else:
                for commandLineOptions in proc.cmdline():
                    if commandLine in commandLineOptions:
                        proc.kill()
                        print "Process : {0} with {1} command line options, has been killed".format(processName, commandLineOptions)
                        result = True
                        break
    return result


def ExtractArchive(fileName, folder):
    if (fileName.endswith(".tgz")):
        tar = tarfile.open(fileName)
        tar.extractall(path=os.path.join(os.getcwd(), folder))
        tar.close()
        print "{0} extracted in {1}".format(fileName, folder)
    else:
        print "Failed to extract {0}".format(fileName)


def replace(filePath, str1, str2):
    for line in fileinput.input(filePath, inplace=1):
        print line.replace(str1, str2)
    sleep(1)
    output = runAUT("cat " + filePath)
    assert (str2 in output)


def catAppFile(platform, appName, filePath):
    if platform is "android":
        output = runAUT(
            "adb shell run-as org.nativescript." +
            appName +
            " cat files/" +
            filePath)
    if platform is "ios":
        output = runAUT(
            "ddb device get-file \"Library/Application Support/LiveSync/" +
            filePath +
            "\" --app org.nativescript." +
            appName)
    return output


def catAppFileOnEmulator(platform, appName, filePath):
    output = runAUT(
        "adb -s emulator-5554 shell run-as org.nativescript." +
        appName +
        " cat files/" +
        filePath)
    return output


def remove(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise


def uninstall_app(appName, platform, fail=True):
    if (platform == "android"):
        output = runAUT("ddb device uninstall org.nativescript." + appName, set_timeout=120)
        if ("[Uninstalling] Status: RemovingApplication" in output):
            print "{0} application successfully uninstalled.".format(appName)
        else:
            if fail:
                raise NameError(
                    "{0} application failed to uninstall.".format(appName))
    else:
        output = runAUT("ideviceinstaller -U " + appName, set_timeout=120)
        if ("Uninstall: Complete" in output):
            print "{0} application successfully uninstalled.".format(appName)
        else:
            if fail:
                raise NameError(
                    "{0} application failed to uninstall.".format(appName))
