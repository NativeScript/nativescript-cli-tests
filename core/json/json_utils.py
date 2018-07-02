import json

from core.osutils.file import File


class Json(object):

    @staticmethod
    def _replace_value(data, k, v):
        """
        Replace value of key inside json object.
        :param data: json object.
        :param k: key.
        :param v: value.
        """
        for key in data.keys():
            if key == k:
                data[key] = v
            elif type(data[key]) is dict:
                Json._replace_value(data[key], k, v)

    @staticmethod
    def read(file_path):
        """
        Read content of json file.
        :param file_path: Path to file.
        :return: Content of file as json object.
        """

        # Check if file exists
        assert File.exists(file_path), 'Failed to find file: ' + file_path

        # Read it...
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def replace(file_path, key, value):
        """
        Replace value of key in json file.
        :param file_path: File path.
        :param key: Key.
        :param value: Desired value.
        """
        with open(file_path, "r+") as jsonFile:
            data = json.load(jsonFile)
            Json._replace_value(data, key, value)
            jsonFile.seek(0)
            json.dump(data, jsonFile, indent=4)
            jsonFile.truncate()
