"""
Wrapper around Folders
"""

import errno
import os
import platform
import shutil

from core.osutils.command import run
from core.osutils.process import Process


class Folder(object):
    @staticmethod
    def create(folder):
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                raise

    @staticmethod
    def cleanup(folder):
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder, False)
            except:
                if os.path.exists(folder):
                    if 'Windows' in platform.platform():
                        output = run('rmdir /s /q \"{0}\"'.format(folder))
                        if ("another process" in output) or ("gradle" in output.lower()):
                            Process.kill(proc_name='node')
                            Process.kill(proc_name='aapt')
                            Process.kill(proc_name='adb')
                            Process.kill_gradle()
                            output = run('rmdir /s /q \"{0}\"'.format(folder))
                            assert 'another process' not in output, "Failed to delete {0}".format(folder)
                            assert 'gradle' not in output.lower(), "Failed to delete {0}".format(folder)
                    else:
                        run('rm -rf ' + folder)

    @staticmethod
    def exists(path):
        if os.path.isdir(path):
            return True
        else:
            return False

    @staticmethod
    def is_empty(path):
        if os.listdir(path) == []:
            return True
        else:
            return False

    @staticmethod
    def get_current_folder():
        current_folder = os.getcwd()
        print "Current dir: " + current_folder
        return current_folder

    @staticmethod
    def navigate_to(folder, relative_from_current_folder=True):
        new_folder = folder
        if relative_from_current_folder:
            new_folder = os.path.join(Folder.get_current_folder(), folder).replace("\"", "")
        print "Navigate to: " + new_folder
        os.chdir(new_folder)

    @staticmethod
    def copy(src, dst):
        try:
            shutil.copytree(src, dst)
        except OSError as exc:  # python >2.5
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else:
                raise
