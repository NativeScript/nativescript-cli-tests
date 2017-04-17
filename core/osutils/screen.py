from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS


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
                    run('screencapture ' + path, )
