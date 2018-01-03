"""
Chrome related commands.
"""
import os

from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.os_type import OSType
from core.osutils.process import Process
from core.settings.settings import TEST_RUN_HOME, CURRENT_OS


class Chrome(object):
    @staticmethod
    def start(url=""):
        if CURRENT_OS is OSType.OSX:
            chrome_path = os.path.join(TEST_RUN_HOME, 'core', 'chrome', 'start_chrome')
            command = "osascript " + chrome_path + " " + url.replace("&", "\&")
            run(command=command, log_level=CommandLogLevel.SILENT)
            print "Open Google Chrome at {0}".format(url)
            Process.wait_until_running(proc_name="Google Chrome", timeout=30)
        elif CURRENT_OS is OSType.LINUX:
            run(command="google-chrome", log_level=CommandLogLevel.SILENT, wait=False)
            Process.wait_until_running(proc_name="chrome", timeout=30)

    @staticmethod
    def stop():
        print "Stop Google Chrome."
        if CURRENT_OS is OSType.OSX:
            Process.kill("Google Chrome")
        elif CURRENT_OS is OSType.LINUX:
            Process.kill("chrome")

    @staticmethod
    def clean_chrome_dev_tools_local_storage():
        print "Clean Chrome Dev Tools Local Storage."
        if CURRENT_OS is OSType.OSX:
            command = "rm -rf ~/Library/Application\ Support/Google/Chrome/Default/Local\ Storage/"
            "chrome-devtools_devtools_0.localstorage*"
            run(command=command, log_level=CommandLogLevel.SILENT)
