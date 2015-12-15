'''
Created on Dec 14, 2015

@author: vchimev
'''


# C0111 - Missing docstring
# pylint: disable=C0111

import os, time


class File(object):

    @classmethod
    def read_file(cls, file_path):
        with open(file_path,'r') as file_to_read:
            output = file_to_read.read()
        return output

    @classmethod
    def write_file(cls, file_path, text):
        with open(file_path,'w') as file_to_write:
            file_to_write.write(text + '\n')

    @classmethod
    def append_file(cls, file_path, text):
        with open(file_path, 'a') as file_to_append:
            file_to_append.write(time.strftime("%X") + text + '\n')

    @classmethod
    def remove_file(cls, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
