import dask
import dask.dataframe as dd
import pandas as pd
from dask.diagnostics import ProgressBar
import argparse
import numpy as np

def compute_agg(df):
    return pd.Series({
        **{
            col+'_p'+str(p): np.float32(np.quantile(df[col], p))
            for col in df.columns if col not in ['id', '5_min_chunk', 'time_of_day', 'weekday', 'quarter', 'count', 'step']
            for p in [0, 0.25, 0.5, 0.75, 1]
        },
        "count": np.int64(len(df))
    })

def compute_agg_meta(df):
    return {
         **{
            col+'_p'+str(p): np.float32
            for col in df.columns if col not in ['id', '5_min_chunk', 'time_of_day', 'weekday', 'quarter', 'count', 'step']
            for p in [0, 0.25, 0.5, 0.75, 1]
        }, 
        "count": np.int64
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='./data/series_train.parquet')
    parser.add_argument('--output', type=str, default='./data/series_train_agg.parquet')
    args = parser.parse_args()

    # dask.config.set({'temporary_directory': './.cache'})

    # pgb = ProgressBar()
    # pgb.register()

    ts = pd.read_parquet(args.data)

    ts['5_min_chunk'] = ts['time_of_day'] // (1e9 * 60 * 5)

    agg_ts = ts.groupby(['id', 'weekday', '5_min_chunk'], observed=True).apply(compute_agg, meta=compute_agg_meta(ts))

    agg_ts.to_parquet(args.output)