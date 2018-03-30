"""
Tests for 'tns resources generate' icons and splashes
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.folder import Folder
from core.osutils.image_utils import ImageUtils
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS
from core.tns.tns import Tns


class ResourcesGenerateTests(BaseClass):
    image_path = os.path.join(os.getcwd(), "data", "images", "resources_generate", "star.png")
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
        Folder.cleanup("temp_ios_resources")

    def test_001_tns_resources_generate_icons(self):
        app_resources_android = os.path.join(os.getcwd(), self.app_name, "app", "App_Resources", "Android")
        app_resources_ios = os.path.join(os.getcwd(), self.app_name, "app", "App_Resources", "iOS", "Assets.xcassets",
                                         "AppIcon.appiconset")

        output = run("tns resources generate icons \"" + self.image_path + "\"" + " --path " + self.app_name)
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
        if CURRENT_OS == OSType.OSX:
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

    def test_002_tns_resources_generate_spalshes(self):
        app_resources_android = os.path.join(os.getcwd(), self.app_name, "app", "App_Resources", "Android")
        app_resources_ios = os.path.join(os.getcwd(), self.app_name, "app", "App_Resources", "iOS", "Assets.xcassets")

        output = run("tns resources generate splashes \"" + self.image_path + "\"" + " --background green --path "
                     + self.app_name)
        assert "Generating splash screens" in output
        assert "Splash screens generation completed" in output

        # Android
        folders = ["drawable-hdpi", "drawable-ldpi", "drawable-mdpi", "drawable-xhdpi", "drawable-xxhdpi",
                   "drawable-xxxhdpi"]

        for folder in folders:
            actual_logo = os.path.join(app_resources_android, folder, "logo.png")
            expected_logo = os.path.join(self.expected_images_android, folder, "logo.png")
            result = ImageUtils.image_match(actual_logo, expected_logo, 0.1)

            if str(result[0]) is "False":
                assert False, "Images: \n{0} and \n{1} \nhas diff: {2}".format(actual_logo, expected_logo,
                                                                               str(result[1]))

            actual_background = os.path.join(app_resources_android, folder, "background.png")
            expected_background = os.path.join(self.expected_images_android, folder, "background.png")
            result = ImageUtils.image_match(actual_background, expected_background, 0.1)

            if str(result[0]) is "False":
                assert False, "Images: \n{0} and \n{1} \nhas diff: {2}".format(actual_background, expected_background,
                                                                               str(result[1]))

        # iOS
        if CURRENT_OS == OSType.OSX:
            # Get all images to compare in one folder
            src_1 = os.path.join(app_resources_ios, "LaunchImage.launchimage")
            src_2 = os.path.join(app_resources_ios, "LaunchScreen.AspectFill.imageset")
            src_3 = os.path.join(app_resources_ios, "LaunchScreen.Center.imageset")

            Folder.create("temp_ios_resources")
            dist = os.path.join(os.getcwd(), "temp_ios_resources")

            Folder.copy(src_1, dist, only_files=True)
            Folder.copy(src_2, dist, only_files=True)
            Folder.copy(src_3, dist, only_files=True)

            ios_images = ["Default-568h@2x.png", "Default-667h@2x.png", "Default-736h@3x.png", "Default-1125h.png",
                          "Default-Landscape-X.png", "Default-Landscape.png", "Default-Landscape@2x.png",
                          "Default-Landscape@3x.png", "Default-Portrait.png", "Default-Portrait@2x.png", "Default.png",
                          "Default@2x.png", "LaunchScreen-AspectFill.png", "LaunchScreen-AspectFill@2x.png",
                          "LaunchScreen-Center.png", "LaunchScreen-Center@2x.png"]

            for image in ios_images:
                actual_image = os.path.join(os.getcwd(), "temp_ios_resources", image)
                expected_image = os.path.join(self.expected_images_ios, image)
                result = ImageUtils.image_match(actual_image, expected_image, 0.1)

                if str(result[0]) is "False":
                    assert False, "Images: \n{0} and \n{1} \nhas diff: {2}".format(actual_image, expected_image,
                                                                                   str(result[1]))
        assert True
