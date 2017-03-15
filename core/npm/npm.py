"""
A wrapper of npm commands.
"""
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.folder import Folder
from core.settings.settings import TEST_RUN_HOME


class Npm(object):
    @staticmethod
    def __run_npm_command(command, folder=None, log_level=CommandLogLevel.COMMAND_ONLY):
        if folder is not None:
            Folder.navigate_to(folder=folder, relative_from_current_folder=True)
        output = run('npm {0}'.format(command), log_level=log_level)
        if folder is not None:
            Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        return output

    @staticmethod
    def install(package, option='', folder=None, log_level=CommandLogLevel.COMMAND_ONLY):
        Npm.__run_npm_command('i {0} {1}'.format(package, option), folder=folder, log_level=log_level)

    @staticmethod
    def uninstall(package, option='', folder=None, log_level=CommandLogLevel.COMMAND_ONLY):
        Npm.__run_npm_command('un {0} {1}'.format(package, option), folder=folder, log_level=log_level)
