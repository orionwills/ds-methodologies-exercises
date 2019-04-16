import env
import pandas as pd

def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''initiates sql connection'''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_mall_data():
    '''gets all the mall customer data'''
    return pd.read_sql('\
        SELECT * from customers',get_connection('mall_customers'))