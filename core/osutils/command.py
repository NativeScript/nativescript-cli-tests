"""
This file contains all the commons.
"""

import os
import threading
import time

from core.osutils.file import File
from core.osutils.process import Process
from core.settings.settings import OUTPUT_FILE, COMMANDS_FILE, COMMAND_TIMEOUT, \
    DEBUG


def run(command, timeout=None, output=True, file_name=None):
    """
    Execute command in subshell.
    """

    def fork_it():
        """
        This function will be emulate in a parallel thread.

        You can redirect the output to one place and the errors to another:
        # dir file.xxx > output.msg 2> output.err

        You can print the errors and standard output to a single file
        by using the "&1" command to redirect the output for STDERR to STDOUT
        and then sending the output from STDOUT to a file:
        # dir file.xxx 1> output.msg 2>&1
        """

        # execute command
        # print "Thread started"
        if output:
            os.system(command + ' 1> output.txt 2>&1')
        else:
            os.system(command)

    # remove output.txt
    File.remove(OUTPUT_FILE)

    # append to commads.txt
    File.append(COMMANDS_FILE, command)

    # prepare command line
    print "##### {0} Executing command : {1}\n".format(time.strftime("%X"), command)
    thread = threading.Thread(target=fork_it)
    thread.start()

    # wait for thread to finish or timeout
    if timeout is None:
        thread.join(COMMAND_TIMEOUT)
    else:
        thread.join(timeout)

    # kill thread
    if thread.is_alive():
        print '##### ERROR: Process has timed out at ', time.strftime("%X")
        Process.kill('node')
        thread.join()

    # get whenever exist in the pipe ?
    pipe_output = 'NOT_COLLECTED'
    if output:
        pipe_output = File.read(OUTPUT_FILE)
    if DEBUG == 1:
        print pipe_output
        print 'Thread finished. Returning ', pipe_output

    print "##### OUTPUT BEGIN #####\n"
    print pipe_output
    print "##### OUTPUT END #####\n"

    if file_name != None:
        File.write(file_name, pipe_output)

    return pipe_output.strip('\r\n')
