"""
A wrapper of Xcode
"""

from core.osutils.command import run
from core.settings.settings import COMMAND_TIMEOUT


class Xcode(object):
    @staticmethod
    def cleanup_cache():
        """Cleanup Xcode cache and derived data"""
        run("rm -rf ~/Library/Developer/Xcode/DerivedData/", COMMAND_TIMEOUT)
        run("sudo find /var/folders/ -type d -name 'com.apple.DeveloperTools' | " +
            "xargs -n 1 -I dir sudo find dir -name \* -type f -delete")
        run("sudo find /var/folders/ -type d -name 'Xcode'")

        # output = run_aut("sudo find /var/folders/ -type d -name 'Xcode'")
        # assert "Xcode" not in output, "Failed to cleanup Xcode cache"
