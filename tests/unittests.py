# C0111 - Missing docstring
# R0201 - Method could be a funct
# pylint: disable=C0111, R0201


import unittest
from core.commons import run
from core.constants import TNS_PATH
from core.folder import Folder
from core.tns import Tns


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

    def test_001_test_init_jasmine(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " test init --framework jasmine --path TNS_App")

        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        # TODO: Verify console output and app files

    def test_002_test_init_mocha(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " test init --framework mocha --path TNS_App")

        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        # TODO: Verify console output and app files

    def test_003_test_init_qunit(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " test init --framework qunit --path TNS_App")

        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        # TODO: Verify console output and app files
