'''
Tests for livesync command in context of iOS simulator
'''

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0111

import psutil, subprocess, time, unittest

from helpers._os_lib import cleanup_folder, replace, cat_app_file
from helpers._tns_lib import ANDROID_RUNTIME_PATH, IOS_RUNTIME_PATH, \
    create_project_add_platform, live_sync, run
from helpers.device import start_simulator, \
    stop_emulators, stop_simulators


class LiveSyncSimulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        stop_emulators()
        stop_simulators()

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('TNS_App')
        start_simulator('iPhone 6s 90')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        stop_simulators()
        cleanup_folder('TNS_App')

    def test_000_test(self):
        pass
