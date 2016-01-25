"""
Wrapper around Folders
"""

import os
import platform
import shutil

from core.osutils.command import run


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
                        run('rmdir /s /q \"{0}\"'.format(folder))
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
    def navigate_to(folder, relative_from__current_folder=True):
        new_folder = folder
        if relative_from__current_folder:
            new_folder = os.path.join(Folder.get_current_folder(), folder).replace("\"", "")
        print "Navigate to: " + new_folder
        os.chdir(new_folder)
