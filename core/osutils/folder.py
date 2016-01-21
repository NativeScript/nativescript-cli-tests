'''
Created on Dec 14, 2015

@author: vchimev
'''


# C0111 - Missing docstring
# pylint: disable=C0111

import os, platform, shutil
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
        try:
            shutil.rmtree(folder, False)
        except OSError:
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
