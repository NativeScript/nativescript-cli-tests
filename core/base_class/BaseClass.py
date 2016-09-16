import os
import sys
import time
import unittest

from core.logger import Logger
from core.osutils.file import File
from core.osutils.folder import Folder


class BaseClass(unittest.TestCase):
    app_name = "TNS_App"
    app_name_appTest = "appTest"

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        File.remove(logfile)
        Folder.cleanup(cls.app_name)
        sys.stdout = sys.stderr = Logger.Logger(logfile)

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
        self._resultForDoCleanups

    @classmethod
    def tearDownClass(cls):
        pass
