import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr
import numpy as np

ts = pd.read_parquet('../data/series_train.parquet')
df = pd.read_csv('../data/train.csv')

means = ts.groupby(['id', 'relative_date_PCIAT'], observed=True)['enmo'].mean().reset_index()

X = ts['relative_date_PCIAT'].unique()
X.sort()
Rs = []
Pvalues = []
for x in X:
    todays_means = means[means['relative_date_PCIAT'] == x]
    pciat_totals = df[df['id'].isin(todays_means['id'])]['PCIAT-PCIAT_Total'].values
    mask = ~np.isnan(pciat_totals) & ~np.isnan(todays_means['enmo'])
    
    if mask.sum() < 2:
        Rs.append(np.nan)
        Pvalues.append(np.nan)
        continue

    r, pvalue = pearsonr(pciat_totals[mask], todays_means['enmo'][mask])

    if np.isnan(r):
        raise ValueError('r is nan')
    
    if pvalue > 0.05:
        Rs.append(np.nan)
        Pvalues.append(np.nan)
        continue

    Rs.append(r)
    Pvalues.append(pvalue)

np.savez('enmo-pciat.npz', X=X, Rs=Rs, Pvalues=Pvalues)

plt.scatter(X, Rs)
plt.show()