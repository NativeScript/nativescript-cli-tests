"""
Tests for --log trace option.
"""

from core.base_class.BaseClass import BaseClass
from core.osutils.folder import Folder
from core.settings.settings import CURRENT_OS, OSType
from core.tns.tns import Tns


class LogtraceTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)
        self.app_id = "org.nativescript.{0}".format(self.app_name.replace("_", ""))

    def test_101_create_project_log_trace(self):
        output = Tns.create_app(self.app_name, log_trace=True, update_modules=False)
        assert "Creating a new NativeScript project with name " + self.app_name in output
        assert "and id org.nativescript.{0} at location".format(self.app_name.replace("_", "")) in output

        if CURRENT_OS == OSType.WINDOWS:
            assert 'spawn: npm.cmd "install"' in output
        else:
            assert 'spawn: npm "install"' in output
        assert "Project " + self.app_name + " was successfully created" in output

    def test_102_platform_add_log_trace(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_add_android(attributes={"--path": self.app_name}, log_trace=True)
        assert "Looking for project in" in output
        assert "Project directory is" in output
        assert "Package: " + self.app_id in output
        assert "Installed Android Targets" in output
        assert "Using Android SDK" in output
        assert "Platform android successfully added." in output
