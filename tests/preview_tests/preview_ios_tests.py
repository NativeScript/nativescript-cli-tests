from core.base_class.BaseClass import BaseClass
from core.preview_app.preview import Preview
from core.device.simulator import Simulator
from core.tns.tns import Tns
from core.device.device import Device
from core.osutils.file import File
from core.tns.tns_platform_type import Platform
from core.settings.settings import OUTPUT_FOLDER, CURRENT_OS, OSType, \
    ANDROID_PATH, IOS_PATH, SUT_FOLDER, CLI_PATH, IOS_INSPECTOR_PATH, SIMULATOR_NAME, SIMULATOR_TYPE, SIMULATOR_SDK, \
    TEST_RUN_HOME, PREVIEW_APP_PATH_ANDROID, PREVIEW_APP_PATH_IOS, EMULATOR_ID

class PreviewCommandTestsIos(BaseClass):

    SIMULATOR_ID = ''

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.kill()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.IOS)

        Preview.get_app_packages()
        Preview.install_preview_app(cls.SIMULATOR_ID, platform=Platform.IOS)

        Tns.create_app(cls.app_name, update_modules=False)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)

    def test_001_tns_preview_ios_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns preview` and take the app url and open it in Preview App
        output = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                        log_trace=True,assert_success=False)
        log = File.read(output)
        url = Preview.get_url(log)
        Preview.run_app(url, SIMULATOR_ID, platform=Platform.IOS)
                              
        strings = ['Start syncing changes for platform ios',
                   'Project successfully prepared (ios)',
                   'Successfully synced changes for platform ios']
        Tns.wait_for_log(log_file=output, string_list=strings, timeout=180, check_interval=10)
