import csv
import os
from unittest import SkipTest

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.osutils.file import File
from core.settings.settings import TEST_RUN_HOME, EMULATOR_ID

VERIFIED_PLUGINS_OUT = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'out')
WORKSPACE = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'workspace')


def read_data():
    csv_file_path = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'data', 'plugins.csv')
    csv_list = tuple(csv.reader(open(csv_file_path, 'rb'), delimiter=','))
    t = [tuple(l) for l in csv_list]
    t.pop(0)
    return t


class RunPluginDemos(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.ensure_available()

    def setUp(self):
        BaseClass.setUp(self)
        Adb.uninstall_all_apps(device_id=EMULATOR_ID)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    @parameterized.expand(read_data())
    def test_apk(self, name, repo, author, android_support, ios_support, downloads, start, demo_repo):
        if not android_support:
            raise SkipTest("Test skipped, plugin '{0}' is iOS only!".format(name))

        plugin_folder = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'out', name)
        apk_file = File.find(base_path=plugin_folder, file_name='.apk', exact_match=False)
        assert apk_file is not '', "Can't find demo app for {0}!".format(name)
        Adb.install(apk_file_path=apk_file, device_id=EMULATOR_ID)
        Adb.monkey(apk_file=apk_file, device_id=EMULATOR_ID)
