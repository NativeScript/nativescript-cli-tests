'''
Created on Dec 14, 2015

@author: vchimev
'''

# C0111 - Missing docstring
# pylint: disable=C0111
import time

import psutil

from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS


class Process(object):
    @staticmethod
    def is_running(proc_name):
        """Check if process is running"""
        result = False
        for proc in psutil.process_iter():
            if proc_name in str(proc):
                result = True
                break
        return result

    @staticmethod
    def wait_until_running(proc_name, timeout):
        """Wait until process is running
        :param proc_name: Process name.
        :param timeout: Timeout in seconds.
        :return: True if running, false if not running.
        """
        running = False
        end_time = time.time() + timeout
        while not running:
            time.sleep(5)
            running = Process.is_running(proc_name)
            if running:
                running = True
                break
            if (running is False) and (time.time() > end_time):
                raise NameError("{0} not running in {1} seconds.", proc_name, timeout)
        return running

    @staticmethod
    def kill(proc_name, proc_cmdline=None):
        if CURRENT_OS is OSType.WINDOWS:
            proc_name += ".exe"
        result = False
        for proc in psutil.process_iter():
            name = ""
            cmdline = ""
            try:
                name = str(proc.name())
                cmdline = str(proc.cmdline())
            except:
                continue
            if proc_name == name:
                if (proc_cmdline is None) or (proc_cmdline is not None and proc_cmdline == cmdline):
                    try:
                        proc.kill()
                        print "Process {0} has been killed.".format(proc_name)
                        result = True
                    except psutil.NoSuchProcess:
                        continue
        return result
