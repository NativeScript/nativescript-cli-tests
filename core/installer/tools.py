"""
Install tools
"""
from core.osutils.command import run
from core.settings.settings import DDB_PATH


class Tools(object):
    @staticmethod
    def install_ddb():
        output = run("ddb")
        if 'Device Debug Bridge' not in output:
            run("npm install -g " + DDB_PATH)
