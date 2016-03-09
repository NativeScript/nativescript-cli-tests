import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH
from core.tns.tns import Tns


class UnitTests(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('TNS_App')

    def tearDown(self):
        Folder.cleanup('TNS_App')

    def test_101_test_init_jasmine(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " test init --framework jasmine --path TNS_App")

        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        output = run("cat TNS_App/package.json")
        assert "karma-jasmine" in output
        assert "jasmine-core" in output

        output = run("cat TNS_App/karma.conf.js")
        assert "frameworks: ['jasmine']" in output

        output = run("cat TNS_App/app/tests/example.js")
        assert "Jasmine test" in output

        assert File.exists("TNS_App/hooks/after-prepare/nativescript-unit-test-runner.js")

    def test_201_test_init_mocha(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " test init --framework mocha --path TNS_App")

        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        output = run("cat TNS_App/package.json")
        assert "karma-chai" in output
        assert "karma-mocha" in output

        output = run("cat TNS_App/karma.conf.js")
        assert "frameworks: ['mocha', 'chai']" in output

        output = run("cat TNS_App/app/tests/example.js")
        assert "Mocha test" in output

        assert File.exists("TNS_App/hooks/after-prepare/nativescript-unit-test-runner.js")

    def test_301_test_init_qunit(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " test init --framework qunit --path TNS_App")

        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        output = run("cat TNS_App/package.json")
        assert "karma-qunit" in output
        assert "qunitjs" in output

        output = run("cat TNS_App/karma.conf.js")
        assert "frameworks: ['qunit']" in output

        output = run("cat TNS_App/app/tests/example.js")
        assert "QUnit test" in output

        assert File.exists("TNS_App/hooks/after-prepare/nativescript-unit-test-runner.js")
