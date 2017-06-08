"""
Perf utils.
"""
import pandas as pd


class PerfUtils(object):
    csv_ext = ".csv"
    png_ext = ".png"

    @classmethod
    def plot_data(cls, csv_file_path, title):
        df = pd.read_csv(csv_file_path)
        data = df['start_time'].tail(15)
        plot = data.plot(legend=False,
                         linewidth=5, rot=23)
        fig = plot.get_figure()
        fig.suptitle(title, fontsize=15)
        fig.savefig(csv_file_path.replace(cls.csv_ext, cls.png_ext))
