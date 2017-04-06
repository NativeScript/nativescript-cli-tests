import os
import sys
import time
import unittest
import shutil

from core.logger import Logger
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import OUTPUT_FOLDER, TEST_RUN_HOME


class BaseClass(unittest.TestCase):
    app_name = "TestApp"
    platforms_android = os.path.join(app_name, "platforms", "android")

    errors = 0
    failures = 0

    @classmethod
    def IsFailed(cls, res):
        is_failed = False

        if len(res.failures) > cls.failures:
            cls.failures = len(res.failures)
            is_failed = True
        if len(res.errors) > cls.errors:
            cls.errors = len(res.errors)
            is_failed = True

        return is_failed

    @classmethod
    def setUpClass(cls, logfile=""):

        Process.kill(proc_name='node', proc_cmdline='tns')

        if logfile == "":
            logfile = os.path.join(OUTPUT_FOLDER, cls.__name__ + ".txt")
        File.remove(logfile)
        sys.stdout = sys.stderr = Logger.Logger(logfile)

        Folder.cleanup(cls.app_name)

    def setUp(self):
        print ""
        print "{0} _________________________________TEST START_______________________________________". \
            format(time.strftime("%X"))
        print ""
        print self._testMethodName
        print ""

    def tearDown(self):
        print ""
        print "{0} ____________________________________TEST END____________________________________". \
            format(time.strftime("%X"))
        print ""
        if self.IsFailed(self._resultForDoCleanups) is True:
            src = os.path.join(TEST_RUN_HOME, self.app_name)
            dest = os.path.join(OUTPUT_FOLDER, self.__class__.__name__ + "_" + self._testMethodName)
            if os.path.isdir(src):
                shutil.copytree(src, dest)
                shutil.rmtree(os.path.join(dest, "platforms"), ignore_errors=True)
                shutil.rmtree(os.path.join(dest, "node_modules"), ignore_errors=True)
            else:
                print "No project " + src

    @classmethod
    def tearDownClass(cls):
        pass
