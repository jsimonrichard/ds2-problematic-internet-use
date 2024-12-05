import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.discriminant_analysis import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

import miceforest as mf
from sklearn.preprocessing import OneHotEncoder

class DataFrameOneHotEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.encoder = None
        self.categorical_columns = None
        self.feature_names = None
    
    def fit(self, X, y=None):
        # Get categorical columns
        self.categorical_columns = X.select_dtypes(include=['object']).columns

        # Fit the encoder
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.encoder.fit(X[self.categorical_columns])

        return self
    
    def transform(self, X):
        X_encoded = self.encoder.transform(X[self.categorical_columns])
        feature_names = self.encoder.get_feature_names_out(self.categorical_columns)
        df_encoded = pd.DataFrame(
            X_encoded,
            columns=feature_names,
            index=X.index
        )
        return pd.concat([X.drop(columns=self.categorical_columns), df_encoded], axis=1)


class MiceForestImputer(BaseEstimator, TransformerMixin):
    def __init__(self, tune=False, random_state=42):
        self.random_state = random_state
        self.kernel = None
        self.tune = tune
    
    def fit(self, X, y=None):
        self.kernel = mf.ImputationKernel(
            data=X.reset_index(drop=True), 
            # variable_schema=X.columns.to_list(), 
            num_datasets=1,
            random_state=self.random_state,
        )
        if self.tune:
            optimal_params = self.kernel.tune_parameters(
                dataset=0, 
                use_gbdt=True,
                num_iterations=500,
                random_state=self.random_state,
            )
            self.kernel.mice(1, variable_parameters=optimal_params)
        else:
            self.kernel.mice(2)
        
        return self
    
    def transform(self, X):
        return self.kernel.transform(X.reset_index(drop=True))