import time

from core.osutils.file import File


class LivesyncHelper(object):
    CHANGE_XML = ['app/main-page.xml', 'TAP', 'TEST']
    CHANGE_JS = ['app/main-view-model.js', 'taps', 'clicks']
    CHANGE_CSS = ['app/app.css', '18', '32']
    CHANGE_LICENSE = ['node_modules/tns-core-modules/LICENSE', 'Copyright', 'MyCopyright']
    CHANGE_TNS_MODULES = ['node_modules/tns-core-modules/application/application-common.js',
                          '(\"globals\");',
                          '(\"globals\"); // test']

    CHANGE_XML_INVALID_SYNTAX = ['app/main-page.xml', '</Page.actionBar>', '</Page.actionBar']

    NG_CHANGE_TS = ['app/item/item.service.ts', 'Ter Stegen', 'Stegen Ter']
    NG_CHANGE_CSS = ['app/app.css', 'core.light.css', 'core.dark.css']
    NG_CHANGE_HTML = ['app/item/items.component.html', '[text]="item.name"', '[text]="item.id"']

    @staticmethod
    def replace(app_name, file_change, sleep=1):
        File.replace(app_name + '/' + file_change[0], file_change[1], file_change[2])
        time.sleep(sleep)

    @staticmethod
    def rollback(app_name, file_change, sleep=1):
        File.replace(app_name + '/' + file_change[0], file_change[2], file_change[1])
        time.sleep(sleep)

    @staticmethod
    def replace_all(app_name):
        LivesyncHelper.replace(app_name, LivesyncHelper.CHANGE_XML)
        LivesyncHelper.replace(app_name, LivesyncHelper.CHANGE_JS)
        LivesyncHelper.replace(app_name, LivesyncHelper.CHANGE_CSS)
        LivesyncHelper.replace(app_name, LivesyncHelper.CHANGE_LICENSE)
        LivesyncHelper.replace(app_name, LivesyncHelper.CHANGE_TNS_MODULES)

    @staticmethod
    def rollback_all(app_name):
        LivesyncHelper.rollback(app_name, LivesyncHelper.CHANGE_XML)
        LivesyncHelper.rollback(app_name, LivesyncHelper.CHANGE_JS)
        LivesyncHelper.rollback(app_name, LivesyncHelper.CHANGE_CSS)
        LivesyncHelper.rollback(app_name, LivesyncHelper.CHANGE_LICENSE)
        LivesyncHelper.rollback(app_name, LivesyncHelper.CHANGE_TNS_MODULES)
