"""
Created on Dec 14, 2015

@author: vchimev
"""

# C0111 - Missing docstring
# pylint: disable=C0111

import errno
import fileinput
import fnmatch
import os
import time
import shutil

from core import osutils
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
            except OSError as err:
                if err.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                    raise

    @staticmethod
    def replace(file_path, str1, str2):
        """Replace strings in file
        :rtype: object
        """
        for line in fileinput.input(file_path, inplace=1):
            print line.replace(str1, str2)
        time.sleep(1)
        print "~~~ Replace ~~~"
        # output = emulate("cat " + file_path)
        # assert str2 in output

    @staticmethod
    def list_of_files_exists(root_folder, files_list, ignore_file_count=True):
        """Check if files in list exists on file system"""

        list_of_file = open('data/files/' + files_list)
        expected_lines = 0
        for line in list_of_file:
            expected_lines += 1
            rel_path = root_folder + '/' + line.rstrip('\r\n')
            print "checking ", rel_path
            if "!" in line:
                if os.path.exists(rel_path):
                    print "File " + rel_path + " exist, this is a problem!"
                    return False
            else:
                if not os.path.exists(rel_path):
                    print "File " + rel_path + " does not exist!"
                    return False
        total = 0
        for root, dirs, files in os.walk(root_folder):
            total += len(files)
            print files
        print "Total files : ", total
        print "Expected lines : ", expected_lines

        if ignore_file_count:
            return True
        else:
            assert expected_lines == total

    @staticmethod
    def string_contains_file_content(output, file_name):
        """
        Check if output string contains content of the file
        """

        out_file = open('data/outputs/' + file_name)
        for line in out_file:
            line = line.rstrip('\r\n')
            print "checking ", line
            if line not in output:
                print "Output does not contain: ", line
                return False
        return True

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
