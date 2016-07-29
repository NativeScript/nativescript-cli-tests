"""
log_trace tests
"""

import unittest

from core.osutils.folder import Folder
from core.tns.tns import Tns


class Logtrace_Tests(unittest.TestCase):
    app_name = "TNS_App"

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./' + self.app_name)

    def tearDown(self):
        pass

    def test_001_create_project_log_trace(self):
        output = Tns.create_app(app_name=self.app_name, log_trace=True)
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
        Tns.create_app(app_name=self.app_name)
        output = Tns.platform_add(platform="android", path=self.app_name, log_trace=True)
        assert "Looking for project in" in output
        assert "Project directory is" in output
        assert "Package: org.nativescript.{0}".format(self.app_name.replace("_", "")) in output
        assert "Available Android targets" in output
        assert "Using Android SDK" in output
        assert "Project successfully created" in output
