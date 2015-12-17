'''
Created on Dec 14, 2015

@author: vchimev
'''


# C0111 - Missing docstring
# pylint: disable=C0111

import os, platform, shutil
from core.commons import run


class Folder(object):

    @classmethod
    def create(cls, folder):
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                raise

    @classmethod
    def cleanup(cls, folder):
        try:
            shutil.rmtree(folder, False)
        except OSError:
            if os.path.exists(folder):
                if 'Windows' in platform.platform():
                    run('rmdir /s /q \"{0}\"'.format(folder))
                else:
                    run('rm -rf ' + folder)

    @classmethod
    def exists(cls, path):
        if os.path.isdir(path):
            return True
        else:
            return False

    @classmethod
    def is_empty(cls, path):
        if os.listdir(path) == []:
            return True
        else:
            return False
