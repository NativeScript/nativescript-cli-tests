"""
A wrapper of Xcode
"""

from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel


class Xcode(object):
    @staticmethod
    def cleanup_cache():
        """
        Cleanup Xcode cache and derived data
        """
        run(command="rm -rf ~/Library/Developer/Xcode/DerivedData/*", log_level=CommandLogLevel.SILENT)

    @staticmethod
    def get_version():
        """
        Get Xcode version
        :return: Version as string.
        """
        output = run(command="xcodebuild -version | head -n 1 | sed -e 's/Xcode //'", log_level=CommandLogLevel.SILENT)
        return int(output.split('.')[0])
