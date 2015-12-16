'''
Created on Dec 14, 2015

@author: vchimev
'''


# C0111 - Missing docstring
# pylint: disable=C0111

import errno, os, shutil


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
        except OSError as err:
            if err.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                raise

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
