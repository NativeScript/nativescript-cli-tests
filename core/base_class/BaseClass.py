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
    app_name_dash = "tns-app"
    app_name_space = "TNS App"
    app_name_symlink = "TNS_AppSymlink"

    app_no_platform = "TNSAppNoPlatform"
    app_name_ios = "my-ios-app"
    app_name_noplatform = "TNS_AppNoPlatform"
    app_name_nosym = "TNSAppNoSym"
    app_template = "template"

    app_name_123 = "123"
    app_name_app = "app"
    platforms_android = os.path.join(app_name, "platforms", "android")

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        File.remove(logfile)
        sys.stdout = sys.stderr = Logger.Logger(logfile)

        Folder.cleanup(cls.app_name)
        Folder.cleanup(cls.app_name_appTest)
        Folder.cleanup(cls.app_name_dash)
        Folder.cleanup(cls.app_name_space)
        Folder.cleanup(cls.app_name_symlink)

        Folder.cleanup(cls.app_no_platform)
        Folder.cleanup(cls.app_name_ios)
        Folder.cleanup(cls.app_name_noplatform)
        Folder.cleanup(cls.app_name_nosym)
        Folder.cleanup(cls.app_template)

        Folder.cleanup(cls.app_name_app)
        Folder.cleanup(cls.app_name_123)

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

    @classmethod
    def tearDownClass(cls):
        pass
