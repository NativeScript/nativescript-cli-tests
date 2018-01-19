"""
A wrapper of npm commands.
"""
import os

from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.os_type import OSType
from core.osutils.process import Process
from core.settings.settings import CURRENT_OS, COMMAND_TIMEOUT


class Gradle(object):
    @staticmethod
    def kill():
        print "Kill gradle processes."
        if CURRENT_OS != OSType.WINDOWS:
            command = "ps -ef  | grep '.gradle/wrapper' | grep -v grep | awk '{ print $2 }' | xargs kill -9"
            run(command=command, log_level=CommandLogLevel.SILENT)
        else:
            print Process.kill(proc_name='java.exe', proc_cmdline='gradle')

    @staticmethod
    def cache_clean():
        print "Clean gradle cache."
        if CURRENT_OS == OSType.WINDOWS:
            run("rmdir /s /q {USERPROFILE}\\.gradle".format(**os.environ), COMMAND_TIMEOUT)
        else:
            run("rm -rf ~/.gradle", 600)
