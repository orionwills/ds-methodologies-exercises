import pandas as pd
import requests
import json

'''
Miscelaneous functions for dealing with Zach's homebrew data
'''

def get_response(url):
    return requests.get(url)

def merge_dfs(df1, df2, how, left, right):
    return pd.merge(df1, df2, how=how, left_on=left, right_on=right)

def clean_up_columns():
    return df.drop(columns=(['store', 'item']))

def get_any(resource):
    base_url = 'https://python.zach.lol'
    df = pd.DataFrame()
    url = 'https://python.zach.lol/api/v1/' + resource
    r = requests.get('https://python.zach.lol/api/v1/' + resource)
    data = r.json()
    if data['payload']['max_page'] == 1:
        df = pd.concat([df, pd.DataFrame(data['payload'][resource])])
    else:
        df = pd.concat([df, pd.DataFrame(data['payload'][resource])])
        r = requests.get(base_url + data['payload']['next_page'])
        data = r.json()
        while data['payload']['page'] <= data['payload']['max_page']:
            df = pd.concat([df, pd.DataFrame(data['payload'][resource])])
            if data['payload']['page'] == data['payload']['max_page']:
                break
            r = requests.get(base_url + data['payload']['next_page'])
            data = r.json()
    df.to_csv(resource + '.csv')
    return df.reset_index(drop=True)

def get_sales(csv):
    base_url = 'https://python.zach.lol'
    df = pd.DataFrame()
    url = 'https://python.zach.lol/api/v1/sales'
    r = requests.get('https://python.zach.lol/api/v1/sales')
    data = r.json()
    df = pd.concat([df, pd.DataFrame(data['payload']['sales'])])
    r = requests.get(base_url + data['payload']['next_page'])
    data = r.json()
    while data['payload']['page'] <= data['payload']['max_page']:
        df = pd.concat([df, pd.DataFrame(data['payload']['sales'])])
        if data['payload']['page'] == data['payload']['max_page']:
            break
        r = requests.get(base_url + data['payload']['next_page'])
        data = r.json()
    df.to_csv(csv)
    return df.reset_index(drop=True)

def get_stores(csv):
    base_url = 'https://python.zach.lol'
    df = pd.DataFrame()
    url = 'https://python.zach.lol/api/v1/stores'
    r = requests.get('https://python.zach.lol/api/v1/stores')
    data = r.json()
    df = pd.concat([df, pd.DataFrame(data['payload']['stores'])])
    df.to_csv(csv)
    return df.reset_index(drop=True)

def get_items(csv):
    base_url = 'https://python.zach.lol'
    df = pd.DataFrame()
    url = 'https://python.zach.lol/api/v1/items'
    r = requests.get('https://python.zach.lol/api/v1/items')
    data = r.json()
    df = pd.concat([df, pd.DataFrame(data['payload']['items'])])
    r = requests.get(base_url + data['payload']['next_page'])
    data = r.json()
    while data['payload']['page'] <= data['payload']['max_page']:
        df = pd.concat([df, pd.DataFrame(data['payload']['items'])])
        if data['payload']['page'] == data['payload']['max_page']:
            break
        r = requests.get(base_url + data['payload']['next_page'])
        data = r.json()
    df.to_csv(csv)
    return df.reset_index(drop=True)