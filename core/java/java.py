"""
A wrapper of java commands.
"""
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel


class Java(object):

    @staticmethod
    def version():
        full_string = run('java -version', log_level=CommandLogLevel.SILENT)
        java_version = (full_string.split('"'))[1].split('.')[:2]
        return '.'.join(java_version)
