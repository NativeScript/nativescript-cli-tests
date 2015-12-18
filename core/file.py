'''
Created on Dec 14, 2015

@author: vchimev
'''


# C0111 - Missing docstring
# pylint: disable=C0111

import errno, os, time
from core.constants import DEFAULT_COMMANDS_FILE

class File(object):

    @classmethod
    def read(cls, file_path):
        with open(file_path, 'r') as file_to_read:
            output = file_to_read.read()
        return output

    @classmethod
    def write(cls, file_path, text):
        with open(file_path, 'w') as file_to_write:
            file_to_write.write(text + '\n')

    @classmethod
    def append(cls, file_path, text):
        with open(file_path, 'a') as file_to_append:
            file_to_append.write(time.strftime("%X") +  ' ' + text + '\n')

    @classmethod
    def exists(cls, path):
        if os.path.exists(path):
            return True
        else:
            return False

    # TODO: from core.commons import run
    @classmethod
    def cat(cls, path):
        command = "cat " + path
        output = os.system(command)
        cls.append(DEFAULT_COMMANDS_FILE, command)
        print command
        return output

    @classmethod
    def extension_exists(cls, path, extension):
        result = False
        for file_name in os.listdir(path):
            if file_name.endswith(extension):
                print "File: {0}".format(os.path.join(path, file_name))
                result = True
                break
        if result:
            print "There is at least one {0} file in {1} directory.".format(extension, path)
        else:
            print "There are no {0} files in {1} directory.".format(extension, path)
        return result

    @classmethod
    def remove(cls, file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as err:
                if err.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                    raise
