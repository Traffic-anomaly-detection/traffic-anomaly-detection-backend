from firebase_admin import db
from firebase_admin import credentials
import firebase_admin
import schedule
import time
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# firebaseConfig = {
#   apiKey: "AIzaSyArYzvqFew8nxMdyN4RvDfZ4Pe_lFY9Y4w",
#   authDomain: "traffic-anomaly-detection.firebaseapp.com",
#   databaseURL: "https://traffic-anomaly-detection-default-rtdb.asia-southeast1.firebasedatabase.app",
#   projectId: "traffic-anomaly-detection",
#   storageBucket: "traffic-anomaly-detection.appspot.com",
#   messagingSenderId: "1010599694991",
#   appId: "1:1010599694991:web:d2c3013e28f7ab1b6716fa",
#   measurementId: "G-VR7QWSMPR8"
# };

PATH = os.getenv('PATH_WEB')
LINE_URL = os.getenv('LINE_URL')
LINE_TOKEN = os.getenv('LINE_TOKEN')

cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://traffic-anomaly-detection-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


df_km127 = pd.read_csv("./dataset/latlon_km127.csv")

ref = db.reference('Accident')
data = {
    'coor': {
        'lat': 113.001,
        'lon': 114.101
    }
}
ref.push(data)


def csv_file():
    header_list = ['datetime', 'road_number', 'km', 'direction', 'all_units', 'inflow_units',
                   'outflow_unit', 'samecell_units', 'avg_speed', 'max_speed', 'avg_traveltime', 'max_traveltime']
    df = pd.read_csv(PATH, names=header_list, parse_dates=["datetime"])
    df = df.drop(['all_units', 'samecell_units', 'max_speed',
                  'avg_traveltime', 'max_traveltime'], axis=1)
    df_traffic = filter_traffic(df)
    df_traffic_wlatlon = map_traffic_with_latlon(df_traffic)
    map_traffic_with_latlon(df_traffic)
    print(df_traffic_wlatlon)
    line_notify()


def filter_traffic(df):
    return df[(df['road_number'] == 1) | (df['road_number'] == 2) | (df['road_number'] == 7)]


def map_traffic_with_latlon(df):
    df['lat'] = df.apply(lambda row: df_km127[(df_km127['rd'] == row['road_number']) & (df_km127['km'] == row['km'])]['lat'].values[0]
                         if len(df_km127[(df_km127['rd'] == row['road_number']) & (df_km127['km'] == row['km'])]['lat'].values) > 0 else 0, axis=1)
    df['lon'] = df.apply(lambda row: df_km127[(df_km127['rd'] == row['road_number']) & (df_km127['km'] == row['km'])]['lon'].values[0]
                         if len(df_km127[(df_km127['rd'] == row['road_number']) & (df_km127['km'] == row['km'])]['lon'].values) > 0 else 0, axis=1)
    return df
    # return df


def line_notify():
    headers = {
        'content-type':
            'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + LINE_TOKEN
    }
    # msg = input("Enter your name:")
    msg = "Send every 2 minutes"
    r = requests.post(LINE_URL, headers=headers, data={'message': msg})
    print(r.text)

# print(df_km127[(df_km127['rd']==1) & (df_km127['km']==815)]['lat'].item())


# schedule.every(2).seconds.do(csv_file)
schedule.every(2).minutes.do(csv_file)
# schedule.every(2).minutes.do(line_notify)
# schedule.every().hour.do(csv_file)
# schedule.every().day.at("10:30").do(csv_file)
# schedule.every(5).to(10).minutes.do(csv_file)
# schedule.every().monday.do(csv_file)
# schedule.every().wednesday.at("13:15").do(csv_file)
# schedule.every().minute.at(":17").do(csv_file)
# csv_file()
# line_notify()
while True:
    schedule.run_pending()
    time.sleep(1)
