"""
Verify getting started templates looks ok
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE, EMULATOR_ID, IOS_PACKAGE, SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.tns import Tns
from core.git.git import Git

class TemplatesTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        Emulator.ensure_available()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)
        Folder.cleanup('template-hello-world')

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    def test_001_template_v2_create_project_local_path(self):
        #https://github.com/NativeScript/nativescript-cli/pull/3793

        Git.clone_repo(repo_url='git@github.com:NativeScript/template-hello-world.git',
                       local_folder="template-hello-world")
        Folder.navigate_to(folder="template-hello-world")
        output = run(command="npm pack")
        Folder.navigate_to(folder=TEST_RUN_HOME, relative_from_current_folder=False)

        Tns.create_app(self.app_name, attributes={'--template': os.path.join('template-hello-world',
                                                                             'tns-template-hello-world-4.2.0.tgz')})
