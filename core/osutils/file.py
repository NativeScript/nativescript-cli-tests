"""
Created on Dec 14, 2015

@author: vchimev
"""

# C0111 - Missing docstring
# pylint: disable=C0111

import fileinput
import fnmatch
import os
import shutil

from core import osutils
from core.osutils.process import Process
from core.settings.settings import TEST_LOG


class File(object):
    @staticmethod
    def read(file_path):
        file_path = file_path.replace("\\", os.path.sep)
        file_path = file_path.replace("/", os.path.sep)
        try:
            with open(file_path, 'r') as file_to_read:
                output = file_to_read.read()
            return output
        except IOError:
            return ""

    @staticmethod
    def write(file_path, text):
        with open(file_path, 'w') as file_to_write:
            file_to_write.write(text + '\n')

    @staticmethod
    def append(file_path, text):
        try:
            with open(file_path, 'a') as file_to_append:
                file_to_append.write(text + os.linesep)
        except IOError:
            pass

    @staticmethod
    def exists(path):
        path = path.replace("\\", os.path.sep)
        path = path.replace("/", os.path.sep)
        if os.path.exists(path):
            return True
        else:
            return False

    @staticmethod
    def pattern_exists(directory, pattern):
        found = False
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    print pattern + " exists: " + filename
                    found = True
        return found

    @staticmethod
    def cat(path):
        command = "cat " + path
        output = osutils.command.run(command)
        File.append(TEST_LOG, command)
        print command
        return output

    @staticmethod
    def extension_exists(path, extension):
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

    @staticmethod
    def remove(file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                print "Failed to delete {0}".format(file_path)
                Process.kill(proc_name='node')
                Process.kill(proc_name='aapt')
                Process.kill_gradle()
                os.remove(file_path)

    @staticmethod
    def replace(file_path, str1, str2):
        """Replace strings in file"""

        for line in fileinput.input(file_path, inplace=1):
            print line.replace(str1, str2)
        print "##### REPLACE FILE CONTENT #####"
        print "File: {0}".format(file_path)
        print "Old String: {0}".format(str1)
        print "New String: {0}".format(str2)

    @staticmethod
    def find_text(text, f):
        data = open(f, 'r')
        found = False
        for line in data:
            if text in line:
                found = True
        return found

    @staticmethod
    def copy(src, dest):
        shutil.copy(src, dest)
