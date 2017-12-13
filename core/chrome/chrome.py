"""
Chrome related commands.
"""
import os

from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.process import Process
from core.settings.settings import TEST_RUN_HOME


class Chrome(object):
    @staticmethod
    def start(url=""):
        command = "osascript " + os.path.join(TEST_RUN_HOME, 'core', 'chrome', 'start_chrome') + " " + url.replace("&", "\&")
        run(command=command, log_level=CommandLogLevel.SILENT)
        print "Open Google Chrome at {0}".format(url)
        Process.wait_until_running(proc_name="Google Chrome", timeout=20)

    @staticmethod
    def stop():
        print "Stop Google Chrome."
        Process.kill("Google Chrome")

    @staticmethod
    def clean_chrome_dev_tools_local_storage():
        print "Clean Chrome Dev Tools Local Storage."
        run("rm -rf ~/Library/Application\ Support/Google/Chrome/Default/Local\ Storage/"
            "chrome-devtools_devtools_0.localstorage*", log_level=CommandLogLevel.SILENT)
