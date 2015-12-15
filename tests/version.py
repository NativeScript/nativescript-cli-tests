# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0111, R0201

import re, unittest
from core.commons import run
from core.constants import TNS_PATH


class Version(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_version(self):
        output = run(TNS_PATH + " --version")
        version = re.compile("^\\d+\\.\\d+\\.\\d+(-\\S+)?$").match(output)
        assert version, "{0} is not a valid version.".format(output)
