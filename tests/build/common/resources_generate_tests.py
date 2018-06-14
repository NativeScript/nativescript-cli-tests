"""
Tests for 'tns resources generate' icons and splashes
"""
import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.folder import Folder
from core.osutils.file import File
from core.osutils.image_utils import ImageUtils
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS, TEST_RUN_HOME
from core.tns.tns import Tns


class ResourcesGenerateTests(BaseClass):
    image_path = os.path.join(TEST_RUN_HOME, "data", "images", "resources_generate", "star.png")

    expected_images = os.path.join(TEST_RUN_HOME, "data", "images", "resources_generate")
    expected_images_android = os.path.join(TEST_RUN_HOME, expected_images, "Android")
    expected_images_ios = os.path.join(TEST_RUN_HOME, expected_images, "iOS")

    app_resources = os.path.join("app", "App_Resources", "Android", "src", "main", "res")
    app_resources_old = os.path.join("app", "App_Resources", "Android")
    assets_base = os.path.join("app", "App_Resources", "iOS", "Assets.xcassets")
    assets_icons = os.path.join(assets_base, "AppIcon.appiconset")

    drawable_folders = ["drawable-hdpi", "drawable-ldpi", "drawable-mdpi", "drawable-xhdpi", "drawable-xxhdpi",
                        "drawable-xxxhdpi"]

    app_based_on_old_template = "TestApp40"

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.create_app(cls.app_name)
        Tns.create_app(cls.app_based_on_old_template, attributes={"--template": "tns-template-hello-world@4.0"})

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_based_on_old_template)
        Folder.cleanup("temp_ios_resources")

    @staticmethod
    def check_icons(app_resources_android, app_resources_ios):
        for folder in ResourcesGenerateTests.drawable_folders:
            actual_icon = os.path.join(app_resources_android, folder, "icon.png")
            expected_icon = os.path.join(ResourcesGenerateTests.expected_images_android, folder, "icon.png")
            result = ImageUtils.image_match(actual_icon, expected_icon, 0.1)

            if str(result[0]) is "False":
                assert False, "Images: \n{0} and \n{1} \nhas diff: {2}".format(actual_icon, expected_icon,
                                                                               str(result[1]))
        # iOS
        if CURRENT_OS == OSType.OSX:
            icons = ["icon-29.png", "icon-29@2x.png", "icon-29@3x.png", "icon-40.png", "icon-40@2x.png",
                     "icon-40@3x.png",
                     "icon-60@2x.png", "icon-60@3x.png", "icon-76.png", "icon-76@2x.png", "icon-83.5@2x.png",
                     "icon-1024.png"]

            for icon in icons:
                actual_icon = os.path.join(app_resources_ios, icon)
                expected_icon = os.path.join(ResourcesGenerateTests.expected_images_ios, icon)
                result = ImageUtils.image_match(actual_icon, expected_icon, 0.1)

                if str(result[0]) is "False":
                    assert False, "Images: \n{0} and \n{1} \nhas diff: {2}".format(actual_icon, expected_icon,
                                                                                   str(result[1]))

    @staticmethod
    def check_splashes(app_resources_android, app_resources_ios):
        for folder in ResourcesGenerateTests.drawable_folders:
            actual_logo = os.path.join(app_resources_android, folder, "logo.png")
            expected_logo = os.path.join(ResourcesGenerateTests.expected_images_android, folder, "logo.png")
            result = ImageUtils.image_match(actual_logo, expected_logo, 0.1)

            if str(result[0]) is "False":
                assert False, "Images: \n{0} and \n{1} \nhas diff: {2}".format(actual_logo, expected_logo,
                                                                               str(result[1]))

            actual_background = os.path.join(app_resources_android, folder, "background.png")
            expected_background = os.path.join(ResourcesGenerateTests.expected_images_android, folder, "background.png")
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
                expected_image = os.path.join(ResourcesGenerateTests.expected_images_ios, image)
                result = ImageUtils.image_match(actual_image, expected_image, 0.1)

                if str(result[0]) is "False":
                    assert False, "Images: \n{0} and \n{1} \nhas diff: {2}".format(actual_image, expected_image,
                                                                                   str(result[1]))

    def test_001_tns_resources_generate_icons(self):
        app_resources_android = os.path.join(TEST_RUN_HOME, self.app_name, self.app_resources)
        app_resources_ios = os.path.join(TEST_RUN_HOME, self.app_name, self.assets_icons)

        output = run("tns resources generate icons \"" + self.image_path + "\"" + " --path " + self.app_name)
        assert "Generating icons" in output
        assert "Icons generation completed" in output

        ResourcesGenerateTests.check_icons(app_resources_android, app_resources_ios)

    def test_002_tns_resources_generate_splashes(self):
        app_resources_android = os.path.join(TEST_RUN_HOME, self.app_name, self.app_resources)
        app_resources_ios = os.path.join(TEST_RUN_HOME, self.app_name, self.assets_base)

        output = run("tns resources generate splashes \"" + self.image_path + "\"" + " --background green --path "
                     + self.app_name)
        assert "Generating splash screens" in output
        assert "Splash screens generation completed" in output

        ResourcesGenerateTests.check_splashes(app_resources_android, app_resources_ios)

    @unittest.skipIf("wait merge")
    def test_003_tns_resources_generate_icons_apetools(self):
        #https://github.com/NativeScript/nativescript-cli/issues/3666
        Folder.cleanup(os.path.join(self.app_name, 'app', 'App_Resources', 'iOS', 'Assets.xcassets',
                                    'AppIcon.appiconset'))
        folder = os.path.join(TEST_RUN_HOME, "data", "images", "resources_generate", "apetool",
                              "AppIcon.appiconset")
        destination = os.path.join(self.app_name, 'app', 'App_Resources', 'iOS', 'Assets.xcassets', 'AppIcon.appiconset')
        Folder.copy(folder, destination)
        icon_path = os.path.join(self.app_name, "app", "App_Resources", "iOS", "Assets.xcassets",
                                 "AppIcon.appiconset", "Icon-76x76@2x.png")

        output = run("tns resources generate icons \"" + icon_path + "\"" + " --path " + self.app_name)
        assert "Generating icons" in output
        assert "Icons generation completed" in output
        assert "Invalid settings specified for the resizer." not in output

    def test_100_tns_resources_generate_icons_old_template_structure(self):
        app_resources_android = os.path.join(TEST_RUN_HOME, self.app_based_on_old_template, self.app_resources_old)
        app_resources_ios = os.path.join(TEST_RUN_HOME, self.app_based_on_old_template, self.assets_icons)

        output = run(
            "tns resources generate icons \"" + self.image_path + "\"" + " --path " + self.app_based_on_old_template)
        assert "Generating icons" in output
        assert "Icons generation completed" in output

        ResourcesGenerateTests.check_icons(app_resources_android, app_resources_ios)
