"""
log_trace tests
"""
import os

from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass
from core.osutils.folder import Folder


class LogtraceTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def test_001_create_project_log_trace(self):
        output = Tns.create_app(self.app_name, log_trace=True, update_modules=False)
        assert "Creating a new NativeScript project with name " + self.app_name in output
        print "and id org.nativescript.{0} at location".format(self.app_name.replace("_", ""))
        assert "and id org.nativescript.{0} at location".format(self.app_name.replace("_", "")) in output

        assert "Using NativeScript verified template:" in output
        assert "tns-template-hello-world with version undefined." in output

        assert "Using custom app from" in output
        assert "Copying custom app into" in output
        assert "Exec npm install tns-core-modules --save --save-exact" in output
        assert "Updating AppResources values" in output
        assert "Project " + self.app_name + " was successfully created" in output

    def test_002_platform_add_log_trace(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.platform_add_android(attributes={"--path":self.app_name}, log_trace=True)
        assert "Looking for project in" in output
        assert "Project directory is" in output
        assert "Package: org.nativescript.{0}".format(self.app_name.replace("_", "")) in output
        assert "Available Android targets" in output
        assert "Using Android SDK" in output
        assert "Project successfully created" in output
