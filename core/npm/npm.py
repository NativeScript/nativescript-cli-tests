"""
A wrapper of npm commands.
"""
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import TEST_RUN_HOME, CURRENT_OS, USE_YARN


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
    def __run_yarn_command(command, folder=None, log_level=CommandLogLevel.FULL):
        if folder is not None:
            Folder.navigate_to(folder=folder, relative_from_current_folder=True)
        output = run('yarn {0}'.format(command), log_level=log_level)
        if folder is not None:
            Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        return output

    @staticmethod
    def version():
        if USE_YARN == "True":
            version = run('yarn -v', log_level=CommandLogLevel.SILENT)
            return int(version.split('.')[0])
        else:
            version = run('npm -v', log_level=CommandLogLevel.SILENT)
            return int(version.split('.')[0])

    @staticmethod
    def pack(folder, output_file):
        try:
            Folder.navigate_to(folder)
            run('npm pack', log_level=CommandLogLevel.SILENT)
            src_file = File.find_by_extension('tgz')[0]
            File.copy(src=src_file, dest=output_file)
            File.remove(src_file)
        except:
            print 'Failed to pack {0}'.format(folder)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)

    @staticmethod
    def install(package='', option='', folder=None, log_level=CommandLogLevel.FULL):
        if USE_YARN == "True":
            if package is None:
                raise NameError('Package can not be None.')
            command = 'add {0} {1}'.format(package, option)
            output = Npm.__run_yarn_command(command, folder=folder, log_level=log_level)
            assert "ERR!" not in output, "`yarn " + command + "` failed with: \n" + output
            return output
        else:
            if package is None:
                raise NameError('Package can not be None.')
            command = 'i {0} {1}'.format(package, option)
            output = Npm.__run_npm_command(command, folder=folder, log_level=log_level)
            assert "ERR!" not in output, "`npm " + command + "` failed with: \n" + output
            return output

    @staticmethod
    def uninstall(package, option='', folder=None, log_level=CommandLogLevel.FULL):
        if USE_YARN == "True":
            if package is None or package is '':
                raise NameError('Package can not be None.')
            return Npm.__run_yarn_command('remove {0} {1}'.format(package, option), folder=folder, log_level=log_level)
        else:
            if package is None or package is '':
                raise NameError('Package can not be None.')
            return Npm.__run_npm_command('un {0} {1}'.format(package, option), folder=folder, log_level=log_level)

    @staticmethod
    def get_version(package):
        if USE_YARN == "True":
            return Npm.__run_yarn_command('info {0} version'.format(package), log_level=CommandLogLevel.SILENT)
        else:
            return Npm.__run_npm_command('show {0} version'.format(package), log_level=CommandLogLevel.SILENT)

    @staticmethod
    def cache_clean():
        if USE_YARN == "True":
            yarn_clean_command = "yarn cache clean"
            print "Clean yarn cache."
            run(yarn_clean_command)
            if CURRENT_OS != OSType.WINDOWS:
                run(command="rm -rf ~/.yarn/tns*")
        else:
            npm_clean_command = "npm cache clean"
            if Npm.version() > 4:
                npm_clean_command = npm_clean_command + " -f"
            print "Clean npm cache."
            run(npm_clean_command)
            if CURRENT_OS != OSType.WINDOWS:
                run(command="rm -rf ~/.npm/tns*")
