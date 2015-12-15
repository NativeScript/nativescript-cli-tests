'''
Created on Dec 14, 2015

@author: vchimev
'''


# C0111 - Missing docstring
# pylint: disable=C0111

import os, shutil, time


class Folder(object):

    @classmethod
    def create_folder(cls, folder):
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                raise

    @classmethod
    def cleanup_folder(cls, folder):
        try:
            shutil.rmtree(folder, False)
            time.sleep(1)
        except:
            raise

    @classmethod
    def folder_exists(cls, path):
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
