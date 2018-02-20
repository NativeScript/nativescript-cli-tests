"""
Process utils.
"""

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
    def is_running_by_commandline(commandline):
        """Check if process with specified commandline is running"""
        result = False
        for proc in psutil.process_iter():
            cmdline = ""
            try:
                cmdline = str(proc.cmdline())
            except:
                continue
            if commandline in cmdline:
                result = True
                break
        return result

    @staticmethod
    def wait_until_running(proc_name, timeout=60):
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
                if (proc_cmdline is None) or (proc_cmdline is not None and proc_cmdline in cmdline):
                    try:
                        proc.kill()
                        print "Process {0} has been killed.".format(proc_name)
                        result = True
                    except psutil.NoSuchProcess:
                        continue
        return result

    @staticmethod
    def kill_by_commandline(cmdline):
        result = False
        for proc in psutil.process_iter():
            cmd = ""
            try:
                name = str(proc.name())
                cmd = str(proc.cmdline())
            except:
                continue
            if (cmdline in cmd):
                try:
                    proc.kill()
                    print "Process {0} has been killed.".format(cmdline)
                    result = True
                except psutil.NoSuchProcess:
                    continue
        return result

    @staticmethod
    def kill_by_handle(file_path):
        for proc in psutil.process_iter():
            try:
                for item in proc.open_files():
                    if file_path in item.path:
                        print "{0} is locked by {1}".format(file_path, proc.name())
                        print "Proc cmd: {0}".format(proc.cmdline())
                        proc.kill()
            except:
                continue

    @staticmethod
    def list():
        for proc in psutil.process_iter():
            name = ""
            cmdline = ""
            try:
                name = str(proc.name())
                cmdline = str(proc.cmdline())
            except:
                continue
            print "{0}  {1}".format(name, cmdline)
