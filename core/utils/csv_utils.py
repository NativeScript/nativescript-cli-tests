"""
CSV utils.
"""
import csv

from core.osutils.file import File


class CsvUtils(object):
    header = ['datetime', 'hostname', 'device_id', 'apk_name', 'app_id', 'start_time']

    @classmethod
    def has_header(cls, file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    if "device_id" == row[2]:
                        return True
                    else:
                        return False
            except csv.Error as e:
                raise IOError('File %s, Line %d: %s' % (file_path, reader.line_num, e))

    @classmethod
    def read(cls, file_path):
        if File.exists(file_path):
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                try:
                    for row in reader:
                        print row
                except csv.Error as e:
                    raise IOError('File %s, Line %d: %s' % (file_path, reader.line_num, e))
        else:
            raise IOError('{0} is not a regular file.'.format(file_path))

    @classmethod
    def write(cls, file_path, rows):
        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            if not cls.has_header(file_path=file_path):
                writer.writerow(cls.header)
            writer.writerow(rows)
