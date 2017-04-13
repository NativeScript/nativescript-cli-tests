from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS


class Screen(object):
    @staticmethod
    def save_screen(path):
        """
        Save screen of host machine.
        :param path: Path where screen will be saved.
        """

        if CURRENT_OS is OSType.LINUX:
            raise NotImplementedError
        else:
            from PIL import ImageGrab
            print 'Save current host screen at {0}'.format(path)
            im = ImageGrab.grab()
            im.save(path)
