import pandas as pd

def convert_to_datetime(df):
    datetime_format = '%a, %d %b %Y %H:%M%S %Z'
    return pd.to_datetime(df, format=datetime_format, utc=True)

def set_date_index(df):
    return df.set_index(df)

def change_to_UTC(series, new_tz):
    return series.tz_localize('utc').tz_convert(new_tz)

def split_date(df):
    df['year'] = df.dt.year
    df['quarter'] = df.dt.quarter
    df['month'] = df.dt.month
    df['day'] = df.dt.day
    df['day_of_week'] = df.dt.day_name().str[:3]
    # df['weekday_or_weekend'] = ((pd.DatetimeIndex(df).dayofweek) < 5).astype(float)
    df['is_weekend'] = (df.weekday.str.startswith('S')).astype(int)
    return df

def sale_total(df):
    df['sale_total'] = df.sale_amount * df.item_price
    return df.rename(columns={'sale_amount': 'quantity'})

def agg_by_weekday(df):
    return df.groupby('weekday')[['sales_total', 'quantity']].agg(['median', 'sum'])

def sale_diff(df):
    df['diff_from_last_day'] = df.sale_total.diff()
    return df

def prep_store_data(df):
    df = convert_to_datetime(df)
    split_date(df)
    sale_total(df)
    sale_diff(df)
    return df