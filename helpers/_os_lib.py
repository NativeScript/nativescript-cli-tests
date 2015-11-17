# W0612 - Unused variable %r
# W0621 - Redefining name from outer scope
# W0702: No exception type(s) specified
# W1401 - Anomalous backslash in string
# E1305 - Too many arguments for format string
# pylint: disable=W0612, W0621, W0702, W1401, E1305
'''
Wraper around OS commands
'''

import errno
import fileinput
import os
import platform
import shutil
import tarfile
import threading
from time import sleep
import time

import psutil

ADB_PATH = os.path.join(os.environ.get('ANDROID_HOME'), 'platform-tools', 'adb')


DEFAULT_TIMEOUT = 180  # seconds
DEFAULT_OUTPUT_FILE = "output.txt"
DEBUG = 0

def run_aut(cmd, set_timeout=None, get_output=True, write_to_file=None):
    '''Run system command'''
    def fork_it():
        '''
        This function will be run in parallel thread.
        You can redirect the output to one place, and the errors to another.
        # dir file.xxx > output.msg 2> output.err
        You can print the errors and standard output to a single file by using the "&1" command to
        redirect the output for STDERR to STDOUT and then sending the output from STDOUT to a file:
        # dir file.xxx 1> output.msg 2>&1
        '''

        print 'Thread started'
        if get_output:
            os.system(cmd + ' 1> output.txt 2>&1')
        else:
            os.system(cmd)

    # prepare command line
    print "##### {0} Executing command : {1}".format(time.strftime("%X"), cmd)
    if os.path.exists(DEFAULT_OUTPUT_FILE):
        os.remove(DEFAULT_OUTPUT_FILE)
    thread = threading.Thread(target=fork_it)
    thread.start()
    # waiting for thread to finish or timeout
    if set_timeout is None:
        thread.join(DEFAULT_TIMEOUT)
    else:
        thread.join(set_timeout)
    if thread.is_alive():
        print '#### Process has timeouted at ', time.strftime("%X")
        # kill node.js instance if tns has started it
        kill_process("node", "tns")
        thread.join()
    # do get whenever exist in the pipe
    out = "NOT_COLLECTED"
    if get_output:
        out_file = open(DEFAULT_OUTPUT_FILE, 'r')
        out = out_file.read()
        out_file.close()
    if DEBUG == 1:
        print out
        print 'Thread finished. Returning ', out

    print "##### OUTPUT BEGIN #####"
    print out
    print "##### OUTPUT END #####"

    if write_to_file != None:
        with open(write_to_file, "w") as text_file:
            text_file.write(out)

    return out.strip('\n\r')

def cleanup_folder(folder):
    '''Cleanup folder'''
    try:
        shutil.rmtree(folder, False)
        sleep(1)
    except:
        if os.path.exists(folder):
            if 'Windows' in platform.platform():
                run_aut('rmdir /s /q \"{}\"'.format(folder))
            else:
                run_aut('rm -rf ' + folder)
            sleep(1)

# Check if output of command contains string from file


def check_output(output, file_name):
    '''Check if output string contains content of the file'''

    out_file = open('testdata/outputs/' + file_name)
    for line in out_file:
        line = line.rstrip('\r\n')
        print "checking ", line
        if line not in output:
            print "Output does not contain: ", line
            return False
    return True


def check_file_exists(root_folder, files_list, ignore_file_count=True):
    '''Check if files in list exists on file system'''

    list_of_file = open('testdata/files/' + files_list)
    expected_lines = 0
    for line in list_of_file:
        expected_lines += 1
        rel_path = root_folder + '/' + line.rstrip('\r\n')
        print "checking ", rel_path
        if not os.path.exists(rel_path):
            print "File " + rel_path + " does not exist!"
            return False
    total = 0
    for root, dirs, files in os.walk(root_folder):
        total += len(files)
        print files
    print "Total files : ", total
    print "Expected lines : ", expected_lines

    if ignore_file_count:
        return True
    else:
        assert expected_lines == total

def is_empty(path):
    '''Check if folder is empty'''
    if os.listdir(path) == []:
        return True
    else:
        return False

def folder_exists(path):
    '''Check if folder exists'''
    if os.path.isdir(path):
        return True
    else:
        return False

def file_exists(path):
    '''Check if file exists'''
    if os.path.exists(path):
        return True
    else:
        return False

def file_with_extension_exists(path, extension):
    '''Check if file with extension exists'''
    count = 0
    for file_name in os.listdir(path):
        if file_name.endswith(extension):
            print "File: {0}".format(os.path.join(path, file_name))
            count += 1
    if count > 0:
        print "There is at least one {0} file in {1} directory.".format(extension, path)
        return True
    else:
        print "There are no {0} files in {1} directory.".format(extension, path)
        return False

def is_running_process(process_name):
    '''Check process is running'''
    result = False
    for proc in psutil.process_iter():
        if process_name in str(proc):
            result = True
    return result

def kill_process(process_name, command_line=None):
    '''Kill process'''
    result = False
    for proc in psutil.process_iter():
        if process_name in str(proc):
            if command_line is None:
                proc.kill()
                print "Process : {0} has been killed".format(process_name)
                result = True
            else:
                for command_line_options in proc.cmdline():
                    if command_line in command_line_options:
                        proc.kill()
                        print "Process : {0} with {1} command line options, " + \
                            "has been killed".format(process_name, command_line_options)
                        result = True
                        break
    return result

def extract_archive(file_name, folder):
    '''Extract archive'''
    if file_name.endswith(".tgz"):
        tar = tarfile.open(file_name)
        tar.extractall(path=os.path.join(os.getcwd(), folder))
        tar.close()
        print "{0} extracted in {1}".format(file_name, folder)
    else:
        print "Failed to extract {0}".format(file_name)

def replace(file_path, str1, str2):
    '''Replace strings in file'''
    for line in fileinput.input(file_path, inplace=1):
        print line.replace(str1, str2)
    sleep(1)
    output = run_aut("cat " + file_path)
    assert str2 in output

def cat_app_file(platform, app_name, file_path):
    '''Return content of file on device'''
    if platform is "android":
        output = run_aut(
            ADB_PATH + " shell run-as org.nativescript." +
            app_name +
            " cat files/" +
            file_path)
    if platform is "ios":
        output = run_aut(
            "ddb device get-file \"Library/Application Support/LiveSync/" +
            file_path +
            "\" --app org.nativescript." +
            app_name)
    return output

def cat_app_file_on_emulator(app_name, file_path):
    '''Return content of file on emulator'''
    output = run_aut(ADB_PATH + " -s emulator-5554 shell run-as org.nativescript." + \
        app_name + " cat files/" + file_path)
    return output

def remove(file_path):
    '''Clean path on file system'''
    try:
        os.remove(file_path)
    except OSError as err:
        if err.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise

def uninstall_app(app_name, platform, fail=True):
    '''Uninstall mobile app'''

    if platform == "android":
        output = run_aut("ddb device uninstall org.nativescript." + app_name, set_timeout=120)
        if "[Uninstalling] Status: RemovingApplication" in output:
            print "{0} application successfully uninstalled.".format(app_name)
        else:
            if fail:
                raise NameError(
                    "{0} application failed to uninstall.".format(app_name))
    else:
        output = run_aut("ideviceinstaller -U " + app_name, set_timeout=120)
        if "Uninstall: Complete" in output:
            print "{0} application successfully uninstalled.".format(app_name)
        else:
            if fail:
                raise NameError(
                    "{0} application failed to uninstall.".format(app_name))

def cleanup_xcode_cache():
    '''Cleanup Xcode cache and derived data'''
    run_aut("rm -rf ~/Library/Developer/Xcode/DerivedData/", 600)
    run_aut("sudo find /var/folders/ -type d -name 'com.apple.DeveloperTools' | " + \
                "xargs -n 1 -I dir sudo find dir -name \* -type f -delete")
    output = run_aut("sudo find /var/folders/ -type d -name 'Xcode'")
    # assert "Xcode" not in output, "Failed to cleanup Xcode cache"
