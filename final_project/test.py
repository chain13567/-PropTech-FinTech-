from flask import Flask, request
import xgboost as xgb
import pandas as pd
import numpy as np
from xy import address_to_latlng
from flask import jsonify
from getdistrict import get_district
from distancexy import get_nearest_trastation, get_nearest_metrostation


# from distancexy import nearest_station

# 加載模型
model = xgb.Booster()  # 初始化模型
model.load_model('xgboost_model.json')  # 加载模型


app = Flask(__name__)

@app.route('/')
def home():
    return app.send_static_file('testhtml.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # 獲取前端發送的json data
    district = get_district(data['address'])
    coord_x, coord_y = address_to_latlng(data['address'],"AIzaSyDCL3TzsWNH48R-DDAqd7fwuy5laXmmkYM")
    nearest_trastation_name, nearest_tradistance = get_nearest_trastation(coord_x, coord_y)
    nearest_metrostation_name, nearest_metrodistance = get_nearest_metrostation(coord_x, coord_y)

    berth = data['berth']
    land_area = data['land_area']
    tot_floor = data['tot_floor']
    room_age = data['room_age']
    build_area = data['build_area']
    room = data['room']

    features = pd.DataFrame({
        'district': [district],
        'coord_x': [coord_x],
        'coord_y': [coord_y],
        'land': [1],
        'build': [1],
        'berth': [berth],
        'land_area': [land_area],
        'tot_floor': [tot_floor],
        'bstate_fg': [4],
        'room_age': [room_age],
        'build_area': [build_area],
        'room': [room],
        'cpi': [105.04],
        'revenue': [600000],
        'nearest_tradistance': [nearest_tradistance],
        'nearest_metrodistance': [nearest_metrodistance]
        })

    features['berth'] = features['berth'].astype(int)
    features['land_area'] = features['land_area'].astype(int)
    features['tot_floor'] = features['tot_floor'].astype(int)
    features['room_age'] = features['room_age'].astype(int)
    features['build_area'] = features['build_area'].astype(int)
    features['room'] = features['room'].astype(int)


    dtest = xgb.DMatrix(features)  # 将数据转换为XGBoost需要的格式
    prediction = model.predict(dtest)  # 进行预测
    prediction = round(prediction.item(), 2)  # 将预测结果舍入为两位小数
    
    result = {
    'prediction': prediction,
    'nearest_trastation_name': nearest_trastation_name,
    'nearest_metrostation_name':nearest_metrostation_name
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

    # result = {
    #     'district':district,
    #     'coord_x': coord_x,
    #     'coord_y': coord_y,
    #     'nearest_trastation_name':nearest_station_name, 
    #     'nearest_tradistance':nearest_distance
    # }