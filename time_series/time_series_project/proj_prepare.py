import pandas as pd
import proj_acquire as aq


def set_date_times(foods,activ,log):

    # df1,df2,df3 = aq.acquire_fitbit()
    foods.index= pd.to_datetime(foods.index)
    activ.index= pd.to_datetime(activ.index)
    log.index= pd.to_datetime(log.index)

    return [foods,activ,log]

def merge_dfs(foods,activ,log):
    merged = pd.merge(activ.reset_index(),log.reset_index(),how='right')
    merged = pd.merge(merged,foods.reset_index(),how='inner')
    return merged

def prepare_fitbit():
    return merge_dfs(*set_date_times(*aq.acquire_fitbit()))

def cleanup(df):
    # rename index to date
    df.rename(columns={'index': 'date'})
    # set date to index
    df.set_index('date', inplace=True)
    # dropping columns with mostly zero information
    to_drop = ['calories', 'carbs', 'fat', 'fiber',
        'protien', 'sodium', 'water']
    df = df.drop(columns=(to_drop))
    # remove commas and convert to float64
    for col in df:
        df[col] = df[col].str.replace(',', '')
        df[col] = df[col].astype('float64')
    # drop NaN rows as we'll be predicting them anyway
    df.dropna(inplace=True)
    return df