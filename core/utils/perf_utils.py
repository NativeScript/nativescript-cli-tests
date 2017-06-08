"""
Perf utils.
"""
import sys

import pandas as pd

file_path = sys.argv[1]  # 'perf_info.csv'
file_name = file_path.replace('.csv', '')
df = pd.read_csv(file_path)
data = df[['datetime', 'start_time']].loc[df['hostname'] == 'mcsofnsbuild07'].tail(15)
plot = data.plot(x='datetime', y='start_time', legend=False,
                 linewidth=5, rot=23, title='start_time')
fig = plot.get_figure()
# fig.set_size_inches(10, 8)
fig.suptitle(file_name, fontsize=15)
fig.savefig(file_name + '.png')
