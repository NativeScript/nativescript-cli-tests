import os

import time

import pytesseract
from PIL import Image

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS, OUTPUT_FOLDER


class Screen(object):

    @staticmethod
    def save_screen(path):
        """
        Save screen of host machine.
        :param path: Path where screen will be saved.
        """
        print 'Save current host screen at {0}'.format(path)
        if CURRENT_OS is OSType.LINUX:
            import os
            os.system("import -window root {0}".format(path))
        else:
            try:
                from PIL import ImageGrab
                im = ImageGrab.grab()
                im.save(path)
            except IOError:
                print 'Failed to take screen of host OS'
                if CURRENT_OS is OSType.OSX:
                    print 'Retry...'
                    run('screencapture ' + path)

    @staticmethod
    def get_screen_text():
        """
        Get text of current screen of host machine.
        :return: All the text visible on screen as string
        """
        base_path = os.path.join(OUTPUT_FOLDER, "images", "host")
        if not File.exists(base_path):
            Folder.create(base_path)
        actual_image_path = os.path.join(base_path, "host_{0}.png".format(time.time()))
        if File.exists(actual_image_path):
            File.remove(actual_image_path)
        Screen.save_screen(path=actual_image_path)
        image = Image.open(actual_image_path)
        text = pytesseract.image_to_string(image.convert('L'))
        return text

    @staticmethod
    def wait_for_text(text, timeout=60):
        """
        Wait for text to be visible screen of host machine.
        :param text: Text that should be visible on the screen.
        :param timeout: Timeout in seconds.
        :return: True if text found, False if not found.
        """
        t_end = time.time() + timeout
        found = False
        actual_text = ""
        while time.time() < t_end:
            actual_text = Screen.get_screen_text()
            if text in actual_text:
                print text + " found the screen!"
                found = True
                break
            else:
                print text + " NOT found the screen!"
                time.sleep(5)
        if not found:
            print "ACTUAL TEXT:"
            print actual_text
        return found
