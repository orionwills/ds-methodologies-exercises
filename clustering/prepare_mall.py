import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def get_upper_outliers(s, k):
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k + iqr
    return s.apply(lambda x: max([x - upper_bound, 0]))

def add_upper_outlier_columns(df, k):
    for col in df.select_dtypes('number'):
        df[col + '_outliers'] = get_upper_outliers(df[col], k)
    return df

def peekatdata(df):
    '''gives cursory sample of dataframe passed'''
    head_df = df.head(5)
    print(head_df)
    tail_df = df.tail(5)
    print(tail_df)
    shape_tuple = df.shape
    print(shape_tuple)
    describe_df = df.describe()
    print(describe_df)
    df.info()

def encode_mall(df):
    '''encodes tech support column into a new enumerated column'''
    for col in ('gender', 'annual_income', 'spending_score'):
        encoder=LabelEncoder()
        encoder.fit(df[col])
        print(col)
        new_col = col + '_encoded'
        print(new_col)
        df[new_col] = encoder.transform(df[col])
    return df