from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.settings.settings import DeviceType

FILE_CHANGE_XML = ["app/main-page.xml", "TAP", "TEST"]
FILE_CHANGE_JS = ["app/main-view-model.js", "taps", "clicks"]
FILE_CHANGE_CSS = ["app/app.css", "30", "33"]
FILE_CHANGE_LICENSE = ["node_modules/tns-core-modules/LICENSE", "Copyright", "MyCopyright"]
FILE_CHANGE_TNS_MODULES = ["node_modules/tns-core-modules/application/application-common.js",
                           "(\"globals\");",
                           "(\"globals\"); // test"]


def replace(app_name, file_change):
    File.replace(app_name + "/" + file_change[0], file_change[1], file_change[2])


def verify_replaced(device_type, app_name, file_change):
    file = file_change[0]
    file = file.replace("node_modules/tns-core-modules", "app/tns_modules")
    text = file_change[2]
    if device_type == DeviceType.EMULATOR:
        Emulator.file_contains(app_name, file, text)
    if device_type == DeviceType.SIMULATOR:
        Simulator.file_contains(app_name, file, text)
    if device_type == DeviceType.ANDROID:
        Device.file_contains("android", app_name, file, text)
    if device_type == DeviceType.IOS:
        Device.file_contains("ios", app_name, file, text)


def replace_all(app_name):
    replace(app_name, FILE_CHANGE_XML)
    replace(app_name, FILE_CHANGE_JS)
    replace(app_name, FILE_CHANGE_CSS)
    replace(app_name, FILE_CHANGE_LICENSE)
    replace(app_name, FILE_CHANGE_TNS_MODULES)

def verify_all_replaced(device_type, app_name):
    verify_replaced(device_type, app_name, FILE_CHANGE_XML)
    verify_replaced(device_type, app_name, FILE_CHANGE_JS)
    verify_replaced(device_type, app_name, FILE_CHANGE_CSS)
    verify_replaced(device_type, app_name, FILE_CHANGE_LICENSE)
    verify_replaced(device_type, app_name, FILE_CHANGE_TNS_MODULES)
