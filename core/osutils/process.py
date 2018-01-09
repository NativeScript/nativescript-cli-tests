"""
Process utils.
"""

import os
import time
from os.path import expanduser

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
    def kill_gradle():
        if CURRENT_OS is OSType.WINDOWS:
            print "Kill gradle daemon!"
            gradle_file_path = None
            user_home = expanduser("~")
            for root, dirs, files in os.walk(user_home):
                for current_file in files:
                    if (current_file == 'gradle.bat') and ('3.' in root):
                        gradle_file_path = os.path.join(root, current_file)
            print gradle_file_path
            if gradle_file_path is not None:
                os.system(gradle_file_path + " --stop")
        else:
            print "No need to kill gradle daemon on OSX."
            pass

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
