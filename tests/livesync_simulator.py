'''
Tests for livesync command in context of iOS simulator
'''

# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0111, R0201

import unittest

from helpers._os_lib import cleanup_folder, replace
from helpers._tns_lib import IOS_RUNTIME_SYMLINK_PATH, \
    create_project_add_platform, live_sync, run
from helpers.device import stop_emulators
from helpers.simulator import create_simulator, delete_simulator, \
    cat_app_file_on_simulator, start_simulator, stop_simulators


class LiveSyncSimulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        stop_emulators()
        stop_simulators()

        delete_simulator('iPhone 6s 90')
        create_simulator('iPhone 6s 90', \
            'iPhone 6s', '9.0')

        start_simulator('iPhone 6s 90')
        cleanup_folder('TNS_App')

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        stop_simulators()
        cleanup_folder('TNS_App')

    def test_000_test(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH)
        run(platform="ios", emulator=True, path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")

        live_sync(
            platform="ios",
            emulator=True,
            path="TNS_App")

        output = cat_app_file_on_simulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
