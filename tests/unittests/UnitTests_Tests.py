import os.path
from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.tns.tns import Tns
from core.settings.strings import *


class UnitTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_101_test_init_jasmine(self):
        Tns.create_app(app_name=self.app_name)
        output = Tns.run_tns_command("test init", attributes={"--framework": "jasmine",
                                                              "--path ": self.app_name})

        assert installed_plugin + " " + nativescript_unit_test_runner in output
        assert test_file_created in output
        assert run_tests_using in output

        output = run("cat " + self.app_name + "/package.json")
        assert "karma-jasmine" in output

        output = run("cat " + self.app_name + "/karma.conf.js")
        assert "frameworks: ['jasmine']" in output

        output = run("cat " + self.app_name + "/app/tests/example.js")
        assert "Jasmine test" in output

        assert File.exists(self.app_name + "/hooks/after-prepare/nativescript-unit-test-runner.js")

    def test_201_test_init_mocha(self):
        Tns.create_app(app_name=self.app_name)
        output = Tns.run_tns_command("test init", attributes={"--framework": "mocha",
                                                              "--path": self.app_name})

        assert installed_plugin + " " + nativescript_unit_test_runner in output
        assert test_file_created in output
        assert run_tests_using in output

        output = run("cat " + self.app_name + "/package.json")
        assert "karma-chai" in output
        assert "karma-mocha" in output

        output = run("cat " + self.app_name + "/karma.conf.js")
        assert "frameworks: ['mocha', 'chai']" in output

        output = run("cat " + self.app_name + "/app/tests/example.js")
        assert "Mocha test" in output

        assert File.exists(self.app_name + "/hooks/after-prepare/nativescript-unit-test-runner.js")

    def test_301_test_init_qunit(self):
        Tns.create_app(app_name=self.app_name)
        output = Tns.run_tns_command("test init", attributes={"--framework": "qunit",
                                                              "--path": self.app_name})

        assert installed_plugin + " " + nativescript_unit_test_runner in output
        assert test_file_created in output
        assert run_tests_using in output

        output = run("cat " + self.app_name + "/package.json")
        assert "karma-qunit" in output

        output = run("cat " + self.app_name + "/karma.conf.js")
        assert "frameworks: ['qunit']" in output

        output = run("cat " + self.app_name + "/app/tests/example.js")
        assert "QUnit test" in output

        assert File.exists(self.app_name + "/hooks/after-prepare/nativescript-unit-test-runner.js")
