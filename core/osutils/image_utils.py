from PIL import Image


class ImageUtils(object):
    @staticmethod
    def image_match(actual_image_path, expected_image_path, tolerance=0.05):
        """
        Compare two images.
        :param actual_image_path: Path to actual image.
        :param expected_image_path: Path to expected image.
        :param tolerance: Tolerance in percents.
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
                actual_pixel = actual_pixels[x, y]
                expected_pixel = expected_pixels[x, y]
                if actual_pixel != expected_pixel:
                    actual_r = actual_pixel[0]
                    actual_g = actual_pixel[1]
                    actual_b = actual_pixel[2]
                    expected_r = expected_pixel[0]
                    expected_g = expected_pixel[1]
                    expected_b = expected_pixel[2]
                    if abs(actual_r + actual_g + actual_b - expected_r - expected_g - expected_b) > 30:
                        diff_pixels += 1
                        diff_image.load()[x, y] = (255, 0, 0)

        diff_percent = 100 * float(diff_pixels) / total_pixels
        if diff_percent < tolerance:
            match = True

        return match, diff_percent, diff_image
