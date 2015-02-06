import os, threading, psutil, time, shutil

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
    if os.path.exists(default_output_file): os.remove(default_output_file)
    thread = threading.Thread(target=forkIt)
    thread.start()
    # waiting for thread to finish or timeout
    if set_timeout == None:
        thread.join(default_timeout)
    else:
        thread.join(set_timeout)
    if thread.is_alive():
        print '#### Process has timeouted at ', time.strftime("%X")
        KillProcess("node", "tns")  # kill node.js instance if tns has started it
        thread.join()
    # do get whenever exist in the pipe
    out = "NOT_COLLECTED"
    if getOutput:
        f = open(default_output_file, 'r'); out = f.read(); f.close()
    if DEBUG == 1:
        print out
        print 'Thread finished. Returning ', out

    print "##### OUTPUT BEGIN #####"
    print out
    print "##### OUTPUT END #####"
    return out.strip('\n\r')

def CleanupFolder(folder):
    shutil.rmtree(folder, True, None)
    
def CheckOutput(output, file):
    f = open('testdata/' + file)
    expected_lines = 0
    for line in f:
        expected_lines += 1
        line = line.rstrip('\r\n')
        print "checking ", line
        if not line in output:
            print "Output does not contain: ", line
            return False
    return True

def CheckFilesExists(rootFolder, listFile):
    f = open('testdata/' + listFile)
    expected_lines = 0
    for line in f:
        expected_lines += 1
        relPath = rootFolder + '/' + line.rstrip('\r\n')
        print "checking ", relPath
        if not os.path.exists(relPath):
            print "File doesnt exist!"
            return False
    total = 0
    for root, dirs, files in os.walk(rootFolder):
        total += len(files)
        print files
    print "Total files : ", total
    print "Expected lines : ", expected_lines
    assert(expected_lines == total)
    return True

def IsRunningProcess(processName):
    result = False
    for proc in psutil.process_iter():
        if processName in str(proc):
            result = True
            
    return result 

def WaitForProcess(processName):
    result = False
    for counter in range(1, 10):
        time.sleep(5)
        if IsRunningProcess(processName):
            result = True 
            break 
    return result;
          
def KillProcess(processName, commandLine=None):
    result = False
    for proc in psutil.process_iter():
        if processName in str(proc):
            if commandLine == None:
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