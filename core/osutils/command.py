"""
This file contains all the commons.
"""
import os
import signal
import subprocess
import time
from datetime import datetime

from core.osutils.subprocess_utils import subprocess_utils
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.settings.settings import OUTPUT_FILE, COMMAND_TIMEOUT, TEST_LOG, OUTPUT_FILE_ASYNC, CURRENT_OS, \
    PROCESS_STARTED


def run(command, timeout=COMMAND_TIMEOUT, output=True, wait=True, log_level=CommandLogLevel.FULL):
    # If wait=False log should be writen
    out_file = OUTPUT_FILE

    if not wait:
        time_string = "_" + datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        out_file = OUTPUT_FILE_ASYNC.replace('.', time_string + '.')
        if CURRENT_OS is OSType.WINDOWS:
            command = command + " 1> " + out_file + " 2>&1"
        elif CURRENT_OS is OSType.LINUX:
            command = command + " 1> " + out_file + " 2>&1 &"
        else:
            command = command + " &> " + out_file + " 2>&1 &"
    else:
        if output:
            command = command + ' 1> ' + out_file + ' 2>&1'

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

    new_subprocess = subprocess.Popen(command,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      # runs in the child
                                      # process before
                                      # the exec(), putting
                                      # the child process into
                                      # its own process group
                                      preexec_fn=os.setpgrp,
                                      shell=True,
                                      cwd=None,
                                      env=None)
    pgid = os.getpgid(new_subprocess.pid)
    if timeout is not None:

        if signal.getsignal(signal.SIGALRM) not in (None, signal.SIG_IGN, signal.SIG_DFL):
            # someone is using a SIGALRM handler!
            ValueError("SIGALRM handler already in use!")

        prevAlarmHandler = signal.getsignal(signal.SIGALRM)

        signal.signal(signal.SIGALRM,
                      lambda sig, frame: subprocess_utils.kill(pgid, prevAlarmHandler))

        # setup handler before scheduling signal, to eliminate a race
        signal.alarm(timeout)

    if wait:
        e = subprocess_utils.wait_process(new_subprocess, prevAlarmHandler)
        subprocess_utils.kill(pgid, prevAlarmHandler)
    else:
        PROCESS_STARTED.append(pgid)

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
