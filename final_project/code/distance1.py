import requests
from pprint import pprint
import json
import math
import pandas as pd
import numpy as np

app_id = 'g11530029-e9992290-936a-4fd5'
app_key = '979aa281-ded9-4ba4-9d08-8e324616e95a'

auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
urltra = "https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/Station?%24format=JSON"
urlmetro = "https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/Station/TRTC?&%24format=JSON"

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return{
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }

class data():

    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')

        return{
            'authorization': 'Bearer '+access_token
        }

# 在此定義一個用於計算距離的函數
def calculate_distance(row, station):
    x = row['coord_x']
    y = row['coord_y']
    lat = station['StationPosition']['PositionLat']
    lon = station['StationPosition']['PositionLon']
    return ((x-lat)**2 + (y-lon)**2)**0.5

def nearest_station(row, stations):
    min_distance = float('inf')
    nearest_station = None
    for station in stations:
        distance = calculate_distance(row, station)
        if distance < min_distance:
            min_distance = distance
            nearest_station = station['StationName']['Zh_tw']
    return pd.Series([nearest_station, min_distance])

if __name__ == '__main__':
    try:
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(urltra, headers=d.get_data_header())
    except:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(urltra, headers=d.get_data_header())    

    datajson = json.loads(data_response.text)
    # print(type(datajson))
    df = pd.read_csv('coidA_ALANDTR_preprocess.csv',encoding='utf-8')

    df[['nearest_trastation', 'nearest_tradistance']] = df.apply(nearest_station, args=(datajson['Stations'],), axis=1)
    # print(df.head(15))

    try:
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(urlmetro, headers=d.get_data_header())
    except:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(urlmetro, headers=d.get_data_header())    

    datametro = json.loads(data_response.text)
    # print(type(datajson))
    df[['nearest_metrostation', 'nearest_metrodistance']] = df.apply(nearest_station, args=(datametro,), axis=1)
    print(df.info())

    df.to_csv('coidA_ALANDTR_preprocess1.csv', index=False, encoding='utf-8-sig')
