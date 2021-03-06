"""
A wrapper of the NativeScript CLI.
"""
import os

from core.npm.npm import Npm
from core.osutils.file import File
from core.settings.settings import SUT_FOLDER, TEST_RUN_HOME


class Cli(object):
    @staticmethod
    def install():
        package = File.find(base_path=SUT_FOLDER, file_name="nativescript")
        output = Npm.install(package=package, folder=TEST_RUN_HOME)
        message = "NativeScript CLI installation failed - \"{e}\" found in output."
        assert "dev-post-install" not in output, message.format(e="dev-post-install")
        cli_path = os.path.join(TEST_RUN_HOME, "node_modules", ".bin", "tns")
        assert File.exists(cli_path), "NativeScript CLI installation failed - tns does not exist."

    @staticmethod
    def uninstall():
        output = Npm.uninstall(package="nativescript", folder=TEST_RUN_HOME)
        print output
