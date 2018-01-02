"""
Wrapper around Folders
"""

import errno
import os
import platform
import shutil
import re

from core.osutils.command import run
from core.osutils.process import Process
from ast import literal_eval


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
                            Process.kill(proc_name='node', proc_cmdline='tns')
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

    @staticmethod
    def move(src, dst):
        try:
            shutil.move(src, dst)
        except OSError as exc:  # python >2.5
            if exc.errno == errno.ENOTDIR:
                shutil.move(src, dst)
            else:
                raise

    @staticmethod
    def has_same_structure(dir_path_1, dir_path_2, ignore_set=set()):
        """
        Compares two directories with option to exclude specific files.
        Also can compare directory and set(). Instead of
        Print the diff files if any.
        :param dir_path_1: Path to dir1
        :param dir_path_2: Path to dir2
        :param ignore_set: Paths to files to exclude while comparing dir1 and dir2. Can use regular expressions.
        """

        in_dir1, in_dir2 = Folder.__compare_directories(dir_path_1, dir_path_2, ignore_set)

        if 0 == len(in_dir1) == len(in_dir2):
            return True
        else:
            Folder.__print_directories_diff(in_dir1, in_dir2, dir_path_1, dir_path_2)
            return False

    @staticmethod
    def __compare_directories(dir1, dir2, ignore_set):
        files_set1 = Folder.__build_files_set(dir1, ignore_set)

        # Compares directly set() without building it from directory
        if type(dir2) is set:
            files_set2 = dir2
        else:
            files_set2 = Folder.__build_files_set(dir2, ignore_set)

        return files_set1 - files_set2, files_set2 - files_set1

    @staticmethod
    def __build_files_set(rootdir, ignore_set):
        root_to_subtract = re.compile(r'^.*?' + rootdir + r'[\\/]{0,1}')

        files_set = set()
        for (dirpath, dirnames, filenames) in os.walk(rootdir):
            for filename in filenames + dirnames:
                full_path = os.path.join(dirpath, filename)
                relative_path = root_to_subtract.sub('', full_path, count=1)

                if Folder.__should_add(relative_path, ignore_set):
                    files_set.add(relative_path)

        return files_set - ignore_set

    @staticmethod
    def __should_add(relative_path, ignore_set):
        for ignore_regex in ignore_set:
            p = re.compile(ignore_regex, re.IGNORECASE)
            if p.match(relative_path):
                return False
        return True

    @staticmethod
    def __print_directories_diff(in_dir1, in_dir2, dir1, dir2):
        Folder.__print_file_diff(in_dir1, dir1)
        Folder.__print_file_diff(in_dir2, dir2)

    @staticmethod
    def __print_file_diff(in_dir, dir):
        if len(in_dir) > 0:
            print '\nFound {} difference in {}:'.format(len(in_dir), dir)
            for relative_path in in_dir:
                print '* {0}'.format(relative_path)

