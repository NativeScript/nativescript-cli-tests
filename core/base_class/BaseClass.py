import os
import shutil
import sys
import time
import unittest

from core.logger import Logger
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.osutils.screen import Screen
from core.settings.settings import OUTPUT_FOLDER, TEST_RUN_HOME


class BaseClass(unittest.TestCase):
    app_name = "TestApp"
    platforms_android = os.path.join(app_name, "platforms", "android")

    errors = 0
    failures = 0

    @classmethod
    def __copy_project_folder(cls, artifacts_folder):
        """
        Archive test app (without platforms and node_modules)
        :param artifacts_folder: Base folder where artifacts from failed tests are stored.
        """
        src = os.path.join(TEST_RUN_HOME, cls.app_name)
        dest = os.path.join(artifacts_folder, cls.app_name)
        if os.path.isdir(src):
            try:
                shutil.copytree(src, dest)
                shutil.rmtree(os.path.join(dest, "platforms"), ignore_errors=True)
                shutil.rmtree(os.path.join(dest, "node_modules"), ignore_errors=True)
            except:
                print "Failed to backup {0}".format(cls.app_name)
        else:
            print "No project " + src

    @classmethod
    def __save_host_screen(cls, artifacts_folder, test_method_name):
        """
        Save screen of desktop host machine
        :param artifacts_folder: Base folder where artifacts from failed tests are stored.
        :param test_method_name: Test method name.
        """
        screen_path = os.path.join(artifacts_folder, "{0}.png".format(test_method_name))
        Screen.save_screen(screen_path)

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
        Process.kill('NativeScript Inspector')
        Process.kill('Safari')
        Process.kill('Xcode')
        Process.kill(proc_name='node', proc_cmdline='tns')

        if logfile == "":
            logfile = os.path.join(OUTPUT_FOLDER, cls.__name__ + ".txt")
        File.remove(logfile)
        sys.stdout = sys.stderr = Logger.Logger(logfile)

        Folder.cleanup(cls.app_name)

    def setUp(self):
        print ""
        print "_________________________________TEST START_______________________________________"
        print "Test Method: {0}".format(self._testMethodName)
        print "Start Time:  {0}".format(time.strftime("%X"))
        print ""

    def tearDown(self):
        # Logic executed only on test failure
        test_name = self._testMethodName
        artifacts_folder = os.path.join(OUTPUT_FOLDER, self.__class__.__name__ + "_" + test_name)
        outcome = "PASSED"
        if self.IsFailed(self._resultForDoCleanups) is True:
            outcome = "FAILED"

            # Ensure `artifacts_folder` exists and it is clean
            if File.exists(artifacts_folder):
                Folder.cleanup(artifacts_folder)
            else:
                Folder.create(artifacts_folder)

            # Collect artifacts on test failure
            self.__copy_project_folder(artifacts_folder=artifacts_folder)
            self.__save_host_screen(artifacts_folder=artifacts_folder, test_method_name=test_name)

        print ""
        print "Test Method: {0}".format(self._testMethodName)
        print "End Time:    {0}".format(time.strftime("%X"))
        print "Outcome:     {0}".format(outcome)
        print "_________________________________TEST END_______________________________________"
        print ""

    @classmethod
    def tearDownClass(cls):
        Process.kill('NativeScript Inspector')
        Process.kill('Safari')
        Process.kill(proc_name='node', proc_cmdline='tns')
