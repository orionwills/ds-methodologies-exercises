import env
import pandas as pd
from IPython.display import display
from PIL import Image
import os.path
from pathlib import Path

DATA_FILE = Path('zillow_data.csv')

def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''initiates sql connection'''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_2016_zillow():
    '''gets all 2016 property data'''
    return pd.read_sql('\
    SELECT p16.*, pred16.logerror, pred16.transactiondate, act.airconditioningdesc, ast.architecturalstyledesc,\
        bct.buildingclassdesc, hst.heatingorsystemdesc, plut.propertylandusedesc, st.storydesc, tct.typeconstructiondesc FROM properties_2016 p16\
	JOIN predictions_2016 pred16 USING(parcelid)\
    LEFT JOIN airconditioningtype act USING(airconditioningtypeid)\
    LEFT JOIN architecturalstyletype ast USING(architecturalstyletypeid)\
    LEFT JOIN buildingclasstype bct USING(buildingclasstypeid)\
    LEFT JOIN heatingorsystemtype hst USING(heatingorsystemtypeid)\
    LEFT JOIN propertylandusetype plut USING(propertylandusetypeid)\
    LEFT JOIN storytype st USING(storytypeid)\
    LEFT JOIN typeconstructiontype tct USING(typeconstructiontypeid)',\
    get_connection('zillow'))

def get_2017_zillow():
    '''gets all 2017 property data'''
    return pd.read_sql('\
    SELECT p17.*, pred17.logerror, pred17.transactiondate, act.airconditioningdesc, ast.architecturalstyledesc,\
        bct.buildingclassdesc, hst.heatingorsystemdesc, plut.propertylandusedesc, st.storydesc, tct.typeconstructiondesc FROM properties_2017 p17\
	JOIN predictions_2017 pred17 USING(parcelid)\
    LEFT JOIN airconditioningtype act USING(airconditioningtypeid)\
    LEFT JOIN architecturalstyletype ast USING(architecturalstyletypeid)\
    LEFT JOIN buildingclasstype bct USING(buildingclasstypeid)\
    LEFT JOIN heatingorsystemtype hst USING(heatingorsystemtypeid)\
    LEFT JOIN propertylandusetype plut USING(propertylandusetypeid)\
    LEFT JOIN storytype st USING(storytypeid)\
    LEFT JOIN typeconstructiontype tct USING(typeconstructiontypeid)',\
    get_connection('zillow'))

def merge_zillow():
    print('--- Gathering 2016 Zillow Data ---')
    df1 = get_2016_zillow()
    print('--- Gathering 2017 Zillow Data ---')
    df2 = get_2017_zillow()
    print('--- Merging 2016 and 2017 Zillow Data ---')
    return df1.append(df2, ignore_index=True)

def drop_columns(df):
    print('--- Dropping null latitude/longitude rows ---')
    df = df[~df.longitude.isnull() | ~df.latitude.isnull()]
    print('--- Dropping id columns ---')
    return df.drop(columns=([\
        'airconditioningtypeid', 'architecturalstyletypeid',\
        'buildingclasstypeid', 'buildingqualitytypeid',
        'decktypeid', 'heatingorsystemtypeid', 'propertylandusetypeid',\
        'storytypeid', 'typeconstructiontypeid'\
    ]))


def acquire_zillow():
    pil_im = Image.open('welcome.png')
    display(pil_im)
    if DATA_FILE.is_file():
        data_type = input(f'Detected {DATA_FILE} - use csv (1) or gather new data (2)? ')
        if data_type == '1':
            print('--- Beginning CSV Import --\n')
            df = pd.read_csv('zillow_data.csv')
            print('--- CSV Import Complete --\n')
            print(f'Shape of DataFrame: {df.shape}')
            return df
        else:
            print('--- Beginning Zillow Data Collection ---')
            df = merge_zillow()
            df = drop_columns(df)
            print('--- Writing to \'zillow_data.csv\' ---')
            df.to_csv('zillow_data.csv', index=False)
            print('--- Data Collection Complete --\n')
            print(f'Shape of DataFrame: {df.shape}')
            return df
    else:
        print('--- Beginning Zillow Data Collection ---')
        df = merge_zillow()
        df = drop_columns(df)
        print('--- Writing to \'zillow_data.csv\' ---')
        df.to_csv('zillow_data.csv', index=False)
        print('--- Data Collection Complete --\n')
        print(f'Shape of DataFrame: {df.shape}')
        return df