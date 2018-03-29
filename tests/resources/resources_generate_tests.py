"""
Tests for 'tns resources generate' icons and splashes
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.folder import Folder
from core.osutils.image_utils import ImageUtils
from core.tns.tns import Tns


class ResourcesGenerateTests(BaseClass):
    image_path = os.path.join(os.getcwd(), "data", "images", "resources_generate", "icon-tulip.png")
    expected_images = os.path.join(os.getcwd(), "data", "images", "resources_generate")
    expected_images_android = os.path.join(os.getcwd(), expected_images, "Android")
    expected_images_ios = os.path.join(os.getcwd(), expected_images, "iOS")

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.create_app(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup("Test App")

    def test_001_tns_resources_generate_icons(self):
        Folder.navigate_to(self.app_name)

        app_resources_android = os.path.join(os.getcwd(), "app", "App_Resources", "Android")
        app_resources_ios = os.path.join(os.getcwd(), "app", "App_Resources", "iOS", "Assets.xcassets",
                                         "AppIcon.appiconset")

        output = run("tns resources generate icons \"" + self.image_path + "\"")
        assert "Generating icons" in output
        assert "Icons generation completed" in output

        # Android
        folders = ["drawable-hdpi", "drawable-ldpi", "drawable-mdpi", "drawable-xhdpi", "drawable-xxhdpi",
                   "drawable-xxxhdpi"]

        for folder in folders:
            actual_icon = os.path.join(app_resources_android, folder, "icon.png")
            expected_icon = os.path.join(self.expected_images_android, folder, "icon.png")
            result = ImageUtils.image_match(actual_icon, expected_icon, 0.1)

            if str(result[0]) is "False":
                assert False, "Images: \n{0} and \n{1} \nhas diff: {2}".format(actual_icon, expected_icon,
                                                                               str(result[1]))
        # iOS
        icons = ["icon-29.png", "icon-29@2x.png", "icon-29@3x.png", "icon-40.png", "icon-40@2x.png", "icon-40@3x.png",
                 "icon-60@2x.png", "icon-60@3x.png", "icon-76.png", "icon-76@2x.png", "icon-83.5@2x.png",
                 "icon-1024.png"]

        for icon in icons:
            actual_icon = os.path.join(app_resources_ios, icon)
            expected_icon = os.path.join(self.expected_images_ios, icon)
            result = ImageUtils.image_match(actual_icon, expected_icon, 0.1)

            if str(result[0]) is "False":
                assert False, "Images: \n{0} and \n{1} \nhas diff: {2}".format(actual_icon, expected_icon,
                                                                               str(result[1]))

        assert True
