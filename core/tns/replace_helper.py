import time

from core.osutils.file import File


class ReplaceHelper(object):
    CHANGE_XML = ["app/main-page.xml", "TAP", "TEST"]
    CHANGE_JS = ["app/main-view-model.js", "taps", "clicks"]
    CHANGE_CSS = ["app/app.css", "42", "99"]
    CHANGE_LICENSE = ["node_modules/tns-core-modules/LICENSE", "Copyright", "MyCopyright"]
    CHANGE_TNS_MODULES = ["node_modules/tns-core-modules/application/application-common.js",
                          "(\"globals\");",
                          "(\"globals\"); // test"]

    CHANGE_XML_INVALID_SYNTAX = ["app/main-page.xml", "</Page>", "</Page"]

    @staticmethod
    def replace(app_name, file_change, sleep=1):
        File.replace(app_name + "/" + file_change[0], file_change[1], file_change[2])
        time.sleep(sleep)

    @staticmethod
    def rollback(app_name, file_change, sleep=1):
        File.replace(app_name + "/" + file_change[0], file_change[2], file_change[1])
        time.sleep(sleep)

    @staticmethod
    def replace_all(app_name):
        ReplaceHelper.replace(app_name, ReplaceHelper.CHANGE_XML)
        ReplaceHelper.replace(app_name, ReplaceHelper.CHANGE_JS)
        ReplaceHelper.replace(app_name, ReplaceHelper.CHANGE_CSS)
        ReplaceHelper.replace(app_name, ReplaceHelper.CHANGE_LICENSE)
        ReplaceHelper.replace(app_name, ReplaceHelper.CHANGE_TNS_MODULES)

    @staticmethod
    def rollback_all(app_name):
        ReplaceHelper.rollback(app_name, ReplaceHelper.CHANGE_XML)
        ReplaceHelper.rollback(app_name, ReplaceHelper.CHANGE_JS)
        ReplaceHelper.rollback(app_name, ReplaceHelper.CHANGE_CSS)
        ReplaceHelper.rollback(app_name, ReplaceHelper.CHANGE_LICENSE)
        ReplaceHelper.rollback(app_name, ReplaceHelper.CHANGE_TNS_MODULES)
