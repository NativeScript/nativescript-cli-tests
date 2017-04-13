from PIL import ImageGrab


class Screen(object):
    @staticmethod
    def save_screen(path):
        """
        Save screen of host machine.
        :param path: Path where screen will be saved.
        """
        print 'Save current host screen at {0}'.format(path)
        im = ImageGrab.grab()
        im.save(path)
