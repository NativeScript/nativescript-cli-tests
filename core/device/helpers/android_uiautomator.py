"""
Wrapper around uiautomator
"""
from core.osutils.process import Process


class UIAuto(object):
    @staticmethod
    def __kill_uiautomator():
        Process.kill(proc_name="adb", proc_cmdline="uiautomator")
        Process.kill(proc_name="adb", proc_cmdline="fork-server")

    @staticmethod
    def __get_device(device_id):
        from uiautomator import Device
        return Device(device_id)

    @staticmethod
    def click(device_id, text, timeout=10):
        """
        Click on text.
        :param device_id: Device identifier.
        :param text: Text
        :param timeout: Timeout to find element before click it.
        """
        d = UIAuto.__get_device(device_id=device_id)
        element = d(text=text)
        if element.wait.exists(timeout=timeout * 1000):
            element.click()
            print 'Click on "{0}"'.format(text)
            UIAuto.__kill_uiautomator()
        else:
            UIAuto.__kill_uiautomator()
            raise NameError("Can't find " + text + " on the screen of " + device_id)

    @staticmethod
    def wait_for_text(device_id, text, timeout=10):
        """
        Wait for text on device.
        :param device_id: Device identifier.
        :param text: Text
        :param timeout: Timeout to find text.
        :return True if text is found, False if text is not found.
        """
        d = UIAuto.__get_device(device_id=device_id)
        found = d(text=text).wait.exists(timeout=timeout * 1000)
        UIAuto.__kill_uiautomator()
        return found
