import pandas as pd

def single_units(df):
    '''trim_to_singles -> trim_by_sqft_bed -> trim_by_roomcnt'''
    return df.pipe(trim_to_singles)\
        .pipe(trim_by_sqft_bed_bth)\
        .pipe(trim_by_roomcnt)\


def trim_to_singles(df):
    '''Removing property types that are typically not considered
    single units'''
    prob_singles = ['Single Family Residential', 'Mobile Home',
                'Manufactured, Modular, Prefabricated Homes',
                'Residential General', 'Townhouse',
                'Planned Unit Development', 'Cluster Home',
                'Cooperative', 'Commercial/Office/Residential Mixed Used',
                'Store/Office (Mixed Use)']
    df = df[df.propertylandusedesc.isin(prob_singles)]
    return df

def trim_by_sqft_bed_bth(df):
    '''Scalding to >500sqft, >0beds, and >0baths'''
    df = df[(df.calculatedfinishedsquarefeet > 500) &
          (df.bedroomcnt > 0) &
          (df.bathroomcnt > 0)]
    return df

def trim_by_roomcnt(df):
    '''Removing properties that have greater than 1 unitcnt
    and dropping all rows that have unitcnt of 0'''
    df = df[(df.unitcnt <2)]
    df = df[~df.unitcnt.isna()]
    return df

def remove_columns(df, cols_to_remove):  
    df = df.drop(columns=cols_to_remove)
    return df

def remove_more_columns(df):
    df.dropna(inplace=True)
    df.drop(columns=(['finishedsquarefeet12', 'fips', 'calculatedbathnbr',
                  'fullbathcnt', 'propertycountylandusecode',
                  'propertyzoningdesc', 'rawcensustractandblock',
                  'structuretaxvaluedollarcnt', 'censustractandblock',
                  'heatingorsystemdesc', 'propertylandusedesc', 'roomcnt',
                  'unitcnt', 'regionidcounty']), inplace=True)
    df.reset_index(inplace=True, drop=True)
    return df

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def zillow_data_prep(df, cols_to_remove=[], prop_required_column=.5, prop_required_row=.75):
    df = remove_columns(df, cols_to_remove)
    df = handle_missing_values(df, prop_required_column, prop_required_row)
    return df

def numeric_to_categorical(df: pd.DataFrame, cols: tuple) -> pd.DataFrame:
    to_coerce = {col: "category" for col in cols}
    return df.astype(to_coerce)

def remove_outliers(df):
    keys = ['bathroomcnt','bedroomcnt','calculatedfinishedsquarefeet',
            'landtaxvaluedollarcnt', 'lotsizesquarefeet',
            'taxvaluedollarcnt', 'taxamount']
    values = [(1,7), (1,7), (500,8000), (10000,2500000),
            (2500, 20000), (25000, 900000), (1000, 17000)]

    dictionary = dict(zip(keys, values))

    for key, value in dictionary.items():
        df = df[df[key] >= value[0]]
        df = df[df[key] <= value[1]]
    return df