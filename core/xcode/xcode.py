"""
A wrapper of Xcode
"""

from core.osutils.command import run
from core.settings.settings import COMMAND_TIMEOUT


class Xcode(object):
    @staticmethod
    def cleanup_cache():
        """
        Cleanup Xcode cache and derived data
        """
        run("rm -rf ~/Library/Developer/Xcode/DerivedData/*", COMMAND_TIMEOUT)

    @staticmethod
    def get_version():
        """
        Get Xcode version
        :return: Version as string.
        """
        output = run("xcodebuild -version | grep Xcode")
        return output.replace("Xcode ", "")
