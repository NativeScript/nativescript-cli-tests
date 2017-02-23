import csv
import os

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.osutils.folder import Folder


def read_data():
    csv_list = tuple(csv.reader(open(os.path.join('plugins', 'plugins.csv'), 'rb'), delimiter=';'))
    t = [tuple(l) for l in csv_list]
    t.pop(0)
    return t


class BuildPlugins_Tests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup(cls.app_name)

    @parameterized.expand(read_data())
    def test_100_build_sample_apps(self, plugin_name, platforms, plugin_repo, plugin_location, plugin_demo_repo,
                                   plugins_to_update, custom_script):
        print plugin_name