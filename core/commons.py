'''
Created on Dec 14, 2015

This file contains all the commons.

@author: vchimev
'''


import os, time, threading
from core.constants import DEBUG, \
    DEFAULT_COMMANDS_FILE, DEFAULT_OUTPUT_FILE, \
    DEFAULT_TIMEOUT
from core.file import File

# TODO: remove this import
from helpers._os_lib import kill_process


def run(cmd, timeout=None, output=True, file_name=None):
    '''
    Execute command in subshell.
    '''

    def fork_it():
        '''
        This function will be run in a parallel thread.

        You can redirect the output to one place and the errors to another:
        # dir file.xxx > output.msg 2> output.err

        You can print the errors and standard output to a single file
        by using the "&1" command to redirect the output for STDERR to STDOUT
        and then sending the output from STDOUT to a file:
        # dir file.xxx 1> output.msg 2>&1
        '''

        # execute command
        # print "Thread started"
        if output:
            os.system(cmd + ' 1> output.txt 2>&1')
        else:
            os.system(cmd)

    # remove output.txt
    File.remove_file(DEFAULT_OUTPUT_FILE)

    # append to commads.txt
    File.append_file(DEFAULT_COMMANDS_FILE, cmd)

    # prepare command line
    print "##### {0} Executing command : {1}\n".format(time.strftime("%X"), cmd)
    thread = threading.Thread(target=fork_it)
    thread.start()

    # wait for thread to finish or timeout
    if timeout is None:
        thread.join(DEFAULT_TIMEOUT)
    else:
        thread.join(timeout)

    # kill thread
    if thread.is_alive():
        print '##### ERROR: Process has timed out at ', time.strftime("%X")
        kill_process('node')
        thread.join()

    # get whenever exist in the pipe ?
    pipe_output = 'NOT_COLLECTED'
    if output:
        pipe_output = File.read_file(DEFAULT_OUTPUT_FILE)
    if DEBUG == 1:
        print pipe_output
        print 'Thread finished. Returning ', pipe_output

    print "##### OUTPUT BEGIN #####\n"
    print pipe_output
    print "##### OUTPUT END #####\n"

    if file_name != None:
        File.write_file(file_name, pipe_output)

    return pipe_output.strip('\r\n')
