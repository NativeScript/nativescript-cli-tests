import unittest
from core.osutils.folder import Folder
from core.logger import Logger
import sys
import time
import os
from core.osutils.file import File


class BaseClass(unittest.TestCase):
    app_name = "TNS_App"
    app_name_appTest = "appTest"

    @classmethod
    def setUpClass(cls):

        logfile = os.path.join("out", cls.__name__ + ".txt")
        File.remove(logfile)
        Folder.cleanup(cls.app_name)
        sys.stdout = sys.stderr = Logger.Logger(logfile)

    #     # setup emulator
    #     Emulator.stop_emulators()
    #     Simulator.stop_simulators()
    #     Emulator.ensure_available()

    #     Folder.cleanup(cls.app_name_appTest)
    #
    #     # setup app
    #     Tns.create_app(cls.app_name, attributes={"--copy-from": "data/apps/livesync-hello-world"})
    #     Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH,
    #                                          "--path": cls.app_name
    #                                          })
    #     Tns.run_android(attributes={"--device": "emulator-5554",
    #                                 "--path": cls.app_name,
    #                                 "--justlaunch": ""})

    def setUp(self):
        print ""
        print "{0} _________________________________TEST START_______________________________________".\
            format(time.strftime("%X"))
        print ""
        print self._testMethodName
        print ""

    def tearDown(self):
        print ""
        print "{0} ____________________________________TEST END____________________________________".\
            format(time.strftime("%X"))
        print ""
        self._resultForDoCleanups

    # @classmethod
    # def tearDownClass(cls):
    #     cls.terminate_watcher()
    #     Emulator.stop_emulators()
    #
    #     Folder.cleanup(cls.app_name)
    #     Folder.cleanup(cls.app_name_appTest)