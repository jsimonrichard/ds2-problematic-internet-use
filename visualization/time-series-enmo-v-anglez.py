import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_parquet('../data/series_train.parquet')

x = df['enmo']
y = df['anglez']

# Calculate the 1st and 99th percentiles for x
x_lower, x_upper = x.min(), np.percentile(x, 95)
y_lower, y_upper = y.min(), y.max()

hist, x_edges, y_edges = np.histogram2d(
    x, y,  
    bins=30,
    range=[[x_lower, x_upper], [y_lower, y_upper]]
)

plt.pcolormesh(x_edges, y_edges, hist.T, cmap='viridis')
plt.colorbar(label='Count')
plt.xlabel('ENMO')
plt.ylabel('AngleZ')

plt.show()
