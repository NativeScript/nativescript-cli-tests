from PIL import Image


class ImageUtils(object):

    @staticmethod
    def image_match(actual_image_path, expected_image_path, tolerance=0.05):
        """
        Compare two images.
        :param actual_image_path: Path to actual image.
        :param expected_image_path: Path to expected image.
        :return: match (boolean value), diff_percent (diff %), diff_image (diff image)
        """
        actual_image = Image.open(actual_image_path)
        actual_pixels = actual_image.load()
        expected_image = Image.open(expected_image_path)
        expected_pixels = expected_image.load()
        width, height = expected_image.size

        total_pixels = width * height
        diff_pixels = 0
        match = False
        diff_image = actual_image.copy()
        for x in range(0, width):
            for y in range(40, height):
                if actual_pixels[x, y] != expected_pixels[x, y]:
                    diff_pixels += 1
                    diff_image.load()[x, y] = (255, 0, 0)

        diff_percent = 100 * float(diff_pixels) / total_pixels
        if diff_percent < tolerance:
            match = True

        return match, diff_percent, diff_image
