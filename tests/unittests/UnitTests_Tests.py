from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.tns.tns import Tns


class UnitTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    def test_101_test_init_jasmine(self):
        Tns.create_app(app_name=self.app_name)
        output = Tns.run_tns_command("test init", attributes={"--framework": "jasmine",
                                                              "--path ": self.app_name})

        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        output = run("cat " + self.app_name + "/package.json")
        assert "karma-jasmine" in output
        assert "jasmine-core" in output

        output = run("cat " + self.app_name + "/karma.conf.js")
        assert "frameworks: ['jasmine']" in output

        output = run("cat " + self.app_name + "/app/tests/example.js")
        assert "Jasmine test" in output

        assert File.exists(self.app_name + "/hooks/after-prepare/nativescript-unit-test-runner.js")

    def test_201_test_init_mocha(self):
        Tns.create_app(app_name=self.app_name)
        output = Tns.run_tns_command("test init", attributes={"--framework": "mocha",
                                                              "--path": self.app_name})

        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

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

        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        output = run("cat " + self.app_name + "/package.json")
        assert "karma-qunit" in output
        assert "qunitjs" in output

        output = run("cat " + self.app_name + "/karma.conf.js")
        assert "frameworks: ['qunit']" in output

        output = run("cat " + self.app_name + "/app/tests/example.js")
        assert "QUnit test" in output

        assert File.exists(self.app_name + "/hooks/after-prepare/nativescript-unit-test-runner.js")
