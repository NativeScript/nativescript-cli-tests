'''
Tests for NativeScript unit tests.
'''

# C0111 - Missing docstring
# R0201 - Method could be a funct
# pylint: disable=C0111, R0201

import unittest

from helpers._os_lib import cleanup_folder
from helpers._tns_lib import create_project, run_aut, TNS_PATH


class UnitTests(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('TNS_App')

#     def tearDown(self):
#         cleanup_folder('TNS_App')

    def test_001_test_init_jasmine(self):
        create_project(proj_name="TNS_App")

        output = run_aut(TNS_PATH + " test init --framework jasmine --path TNS_App")
        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        # TODO: Verify console output and app files

    def test_002_test_init_mocha(self):
        create_project(proj_name="TNS_App")

        output = run_aut(TNS_PATH + " test init --framework mocha --path TNS_App")
        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        # TODO: Verify console output and app files

    def test_003_test_init_qunit(self):
        create_project(proj_name="TNS_App")

        output = run_aut(TNS_PATH + " test init --framework qunit --path TNS_App")
        assert "Successfully installed plugin nativescript-unit-test-runner." in output
        assert "Example test file created in app/tests/" in output
        assert "Run your tests using the \"$ tns test <platform>\" command." in output

        # TODO: Verify console output and app files
