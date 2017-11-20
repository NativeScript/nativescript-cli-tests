"""
A wrapper of npm commands.
"""
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import TEST_RUN_HOME, CURRENT_OS


class Npm(object):
    @staticmethod
    def __run_npm_command(command, folder=None, log_level=CommandLogLevel.FULL):
        if folder is not None:
            Folder.navigate_to(folder=folder, relative_from_current_folder=True)
        output = run('npm {0}'.format(command), log_level=log_level)
        if folder is not None:
            Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        return output

    @staticmethod
    def version():
        version = run('npm -v', log_level=CommandLogLevel.SILENT)
        return int(version.split('.')[0])

    @staticmethod
    def pack(folder, output_file):
        try:
            Folder.navigate_to(folder)
            run('npm pack', log_level=CommandLogLevel.SILENT)
            src_file = File.find_by_extention('tgz')[0]
            File.copy(src=src_file, dest=output_file)
            File.remove(src_file)
        except:
            print "Failed to pack {0}".format(folder)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)

    @staticmethod
    def install(package='', option='', folder=None, log_level=CommandLogLevel.FULL):
        return Npm.__run_npm_command('i {0} {1}'.format(package, option), folder=folder, log_level=log_level)

    @staticmethod
    def uninstall(package, option='', folder=None, log_level=CommandLogLevel.FULL):
        return Npm.__run_npm_command('un {0} {1}'.format(package, option), folder=folder, log_level=log_level)

    @staticmethod
    def cache_clean():
        print "Clean npm cache."
        if CURRENT_OS == OSType.WINDOWS:
            run(command="npm cache clean")
        else:
            run(command="npm cache clean")
            run(command="rm -rf ~/.npm/tns*")
