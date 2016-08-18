"""
Test for version command
"""

import re
import unittest

from core.tns.tns import Tns


class Version_Tests(unittest.TestCase):
    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_version(self):
        output = Tns.run_tns_command("",attributes={"--version": ""})
        version = re.compile("^\\d+\\.\\d+\\.\\d+(-\\S+)?$").match(output)
        assert version, "{0} is not a valid version.".format(output)
