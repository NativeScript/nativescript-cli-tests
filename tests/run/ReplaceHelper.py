from core.osutils.file import File


class ReplaceHelper(object):
    FILE_CHANGE_XML = ["app/main-page.xml", "TAP", "TEST"]
    FILE_CHANGE_JS = ["app/main-view-model.js", "taps", "clicks"]
    FILE_CHANGE_CSS = ["app/app.css", "42", "99"]
    FILE_CHANGE_LICENSE = ["node_modules/tns-core-modules/LICENSE", "Copyright", "MyCopyright"]
    FILE_CHANGE_TNS_MODULES = ["node_modules/tns-core-modules/application/application-common.js",
                               "(\"globals\");",
                               "(\"globals\"); // test"]

    @staticmethod
    def replace(app_name, file_change):
        File.replace(app_name + "/" + file_change[0], file_change[1], file_change[2])

    @staticmethod
    def rollback(app_name, file_change):
        File.replace(app_name + "/" + file_change[0], file_change[2], file_change[1])

    @staticmethod
    def replace_all(app_name):
        ReplaceHelper.replace(app_name, ReplaceHelper.FILE_CHANGE_XML)
        ReplaceHelper.replace(app_name, ReplaceHelper.FILE_CHANGE_JS)
        ReplaceHelper.replace(app_name, ReplaceHelper.FILE_CHANGE_CSS)
        ReplaceHelper.replace(app_name, ReplaceHelper.FILE_CHANGE_LICENSE)
        ReplaceHelper.replace(app_name, ReplaceHelper.FILE_CHANGE_TNS_MODULES)

    @staticmethod
    def rollback_all(app_name):
        ReplaceHelper.rollback(app_name, ReplaceHelper.FILE_CHANGE_XML)
        ReplaceHelper.rollback(app_name, ReplaceHelper.FILE_CHANGE_JS)
        ReplaceHelper.rollback(app_name, ReplaceHelper.FILE_CHANGE_CSS)
        ReplaceHelper.rollback(app_name, ReplaceHelper.FILE_CHANGE_LICENSE)
        ReplaceHelper.rollback(app_name, ReplaceHelper.FILE_CHANGE_TNS_MODULES)

        # @staticmethod
        # def verify_replaced(device_type, app_name, file_change):
        #     file = file_change[0]
        #     file = file.replace("node_modules/tns-core-modules", "app/tns_modules")
        #     text = file_change[2]
        #     if device_type == DeviceType.EMULATOR:
        #         Emulator.file_contains(app_name, file, text)
        #     if device_type == DeviceType.SIMULATOR:
        #         Simulator.file_contains(app_name, file, text)
        #     if device_type == DeviceType.ANDROID:
        #         Device.file_contains(platform="android", app_name=app_name, file_path=file, text=text)
        #     if device_type == DeviceType.IOS:
        #         Device.file_contains(platform="ios", app_name=app_name, file_path=file, text=text)
        #
        # @staticmethod
        # def verify_all_replaced(device_type, app_name, syncAllFiles=False):
        #     ReplaceHelper.verify_replaced(device_type, app_name, ReplaceHelper.FILE_CHANGE_XML)
        #     ReplaceHelper.verify_replaced(device_type, app_name, ReplaceHelper.FILE_CHANGE_JS)
        #     ReplaceHelper.verify_replaced(device_type, app_name, ReplaceHelper.FILE_CHANGE_CSS)
        #     if syncAllFiles:
        #         ReplaceHelper.verify_replaced(device_type, app_name, ReplaceHelper.FILE_CHANGE_LICENSE)
        #         ReplaceHelper.verify_replaced(device_type, app_name, ReplaceHelper.FILE_CHANGE_TNS_MODULES)
