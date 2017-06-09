"""
CSV utils.
"""
import csv
import heapq

import pandas as pd

from core.osutils.file import File


class CsvUtils(object):
    header = ['datetime', 'hostname', 'device_id', 'apk_name', 'app_id', 'start_time']

    @classmethod
    def analyze_data(cls, file_path):
        df = pd.read_csv(file_path)
        start_times = df['start_time'].tolist()
        largest_times = heapq.nlargest(2, start_times)
        smallest_times = heapq.nsmallest(2, start_times)
        peak = (largest_times[0] - largest_times[1] > 250)
        depth = (smallest_times[1] - smallest_times[0] > 250)
        reader = csv.reader(open(file_path, "r"))
        with open((file_path.replace('tmp', 'final')), "a") as f:
            writer = csv.writer(f)
            for row in reader:
                if "device_id" not in row:
                    if peak:
                        print "Peak!"
                        if str(largest_times[0]) not in row:
                            writer.writerow(row)
                    elif depth:
                        print "Depth!"
                        if str(smallest_times[0]) not in row:
                            writer.writerow(row)
                    else:
                        writer.writerow(row)

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
    def write(cls, file_path, rows):
        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            if not cls.has_header(file_path=file_path):
                writer.writerow(cls.header)
            writer.writerow(rows)
