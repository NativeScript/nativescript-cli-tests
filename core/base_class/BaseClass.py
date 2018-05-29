import os
import shutil
import sys
import time
import unittest
from os import listdir

from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.gradle.gradle import Gradle
from core.logger import Logger
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.osutils.process import Process
from core.osutils.screen import Screen
from core.settings.settings import OUTPUT_FOLDER, TEST_RUN_HOME, CURRENT_OS
from core.tns.tns import Tns


class BaseClass(unittest.TestCase):
    app_name = "TestApp"
    app_name_ts = "TestAppTS"
    app_name_ng = "TestAppNG"

    errors = 0
    failures = 0

    @classmethod
    def __copy_images(cls, artifacts_folder):
        """
        Archive test app (without platforms and node_modules)
        :param artifacts_folder: Base folder where artifacts from failed tests are stored.
        """
        src = os.path.join(TEST_RUN_HOME, 'out', 'images')
        dest = os.path.join(artifacts_folder, 'artifacts')
        if os.path.isdir(src):
            try:
                shutil.copytree(src, dest)
                Folder.cleanup(src)
            except:
                print "Failed to backup images and logs."
        else:
            print "No images and logs data."

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
                for file_or_folder in listdir(src):
                    if os.path.isdir(os.path.join(src, file_or_folder)):
                        if file_or_folder != "platforms" and file_or_folder != "node_modules":
                            shutil.copytree(os.path.join(src, file_or_folder), os.path.join(dest, file_or_folder))
                    else:
                        shutil.copyfile(os.path.join(src, file_or_folder), os.path.join(dest, file_or_folder))
            except Exception as e:
                print "Failed to backup {0}. Exception is {1}.".format(cls.app_name, e)
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
    def setUpClass(cls, class_name):

        print ""
        print "_________________________________CLASS START_______________________________________"
        print "Class Name: {0}".format(class_name)
        print "Start Time:  {0}".format(time.strftime("%X"))
        print ""

        Tns.kill()
        Gradle.kill()
        Process.kill('node')
        Process.kill('adb')
        if CURRENT_OS == OSType.OSX:
            Process.kill('NativeScript Inspector')
            Process.kill('Safari')
            Process.kill('Xcode')

        if class_name is not None:
            logfile = os.path.join('out', class_name + '.txt')
        else:
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
        Folder.cleanup(os.path.join(TEST_RUN_HOME, 'out', 'images'))

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
            self.__copy_images(artifacts_folder=artifacts_folder)
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
        Tns.kill()
        Emulator.stop()
        Gradle.kill()
        if CURRENT_OS == OSType.OSX:
            Process.kill('NativeScript Inspector')
            Process.kill('Safari')
            Simulator.stop()
