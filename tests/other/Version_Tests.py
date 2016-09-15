"""
Test for version command
"""

import re

from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass


class Version_Tests(BaseClass):
    def test_001_version(self):
        output = Tns.run_tns_command("",attributes={"--version": ""})
        version = re.compile("^\\d+\\.\\d+\\.\\d+(-\\S+)?$").match(output)
        assert version, "{0} is not a valid version.".format(output)
