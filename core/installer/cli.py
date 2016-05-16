"""
A wrapper of the NativeScript CLI.
"""
import os

from core.osutils.command import run
from core.osutils.file import File
from core.settings.settings import SUT_ROOT_FOLDER


class Cli(object):
    @staticmethod
    def install():
        output = run("npm i " + SUT_ROOT_FOLDER + os.path.sep + "nativescript.tgz")
        message = "NativeScript CLI installation failed - \"{e}\" found in output."
        if "npm ERR! registry error parsing json" not in output:
            assert "ERR" not in output, message.format(e="ERR")
        assert "FiberFuture" not in output, message.format(e="FiberFuture")
        assert "dev-post-install" not in output, message.format(e="dev-post-install")
        assert File.exists("node_modules/.bin/tns"), \
            "NativeScript CLI installation failed - tns does not exist."
        print output

    @staticmethod
    def uninstall():
        output = run("npm uninstall nativescript")
        print output
