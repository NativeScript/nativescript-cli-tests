"""
This file contains all the commons.
"""

import os
import threading
import time
from datetime import datetime

from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.osutils.process import Process
from core.settings.settings import OUTPUT_FILE, COMMAND_TIMEOUT, TEST_LOG, OUTPUT_FILE_ASYNC, CURRENT_OS


def run(command, timeout=COMMAND_TIMEOUT, output=True, wait=True, log_level=CommandLogLevel.FULL):
    """
    Execute command in shell.
    :param command: Command to be executed.
    :param timeout: Timeout for command execution.
    :param output:
    :param wait: Specify if method should wait until command execution complete.
    :param log_level: CommandLogLevel value (SILENT, COMMAND_ONLY, FULL).
    :return: If wait=True return output of the command, else return path to file where command writes log.
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
            os.system(command + ' 1> ' + out_file + ' 2>&1')
        else:
            os.system(command)

    # If wait=False log should be writen
    out_file = OUTPUT_FILE
    if not wait:
        time_string = "_" + datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        out_file = OUTPUT_FILE_ASYNC.replace('.', time_string + '.')
        if CURRENT_OS is OSType.WINDOWS:
            command = command + " 1> " + out_file + " 2>&1"
        else:
            command = command + " &> " + out_file + " 2>&1 &"

    # remove output.txt
    try:
        File.remove(out_file)
    except OSError:
        print "Failed to delete " + out_file
        time.sleep(1)
        File.remove(out_file)

    # log command that is executed (and append to TEST_LOG file)
    if log_level is not CommandLogLevel.SILENT:
        File.append(TEST_LOG, command)
        print "##### {0} Executing command : {1}\n".format(time.strftime("%X"), command)

    # Hack for async commands on Windows
    if CURRENT_OS is OSType.WINDOWS:
        if not wait:
            timeout = 10

    # prepare command line
    thread = threading.Thread(target=fork_it)
    thread.start()

    # wait for thread to finish or timeout
    thread.join(timeout)

    # kill thread if it exceed the timeout
    if thread.is_alive():
        if wait:
            Process.kill_by_commandline(command.partition(' ')[0].rpartition(os.sep)[-1])
            thread.join()
            raise NameError('Process has timed out at ' + time.strftime("%X"))

    # get whenever exist in the pipe ?
    pipe_output = 'NOT_COLLECTED'
    if output:
        pipe_output = File.read(out_file)

    if (log_level is CommandLogLevel.FULL) and wait:
        print "##### OUTPUT BEGIN #####\n"
        print pipe_output
        print "##### OUTPUT END #####\n"

    if wait:
        return pipe_output.strip('\r\n')
    else:
        return out_file
