from datetime import datetime
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

PATH = os.getenv('PATH_WEB')
LINE_URL = os.getenv('LINE_URL')
LINE_TOKEN = os.getenv('LINE_TOKEN')
DB_URL = os.getenv('DB_URL')

cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': DB_URL
})


df_km127 = pd.read_csv("./dataset/latlon_km127.csv")


def csv_file():
    header_list = ['datetime', 'road_number', 'km', 'direction', 'all_units', 'inflow_units',
                   'outflow_unit', 'samecell_units', 'avg_speed', 'max_speed', 'avg_traveltime', 'max_traveltime']
    df = pd.read_csv(PATH, names=header_list, parse_dates=["datetime"])
    df = df.drop(['all_units', 'samecell_units', 'max_speed',
                  'avg_traveltime', 'max_traveltime'], axis=1)
    df_traffic = filter_traffic(df)
    df_traffic_wlatlon = map_traffic_with_latlon(df_traffic)
    print(df_traffic_wlatlon)
    acclat = str(df_traffic_wlatlon.loc[0, 'lat'])
    acclon = str(df_traffic_wlatlon.loc[0, 'lon'])
    accdate = str(df_traffic_wlatlon.loc[0, 'datetime'])
    post_db(accdate, acclat, acclon)
    line_notify(acclat, acclon, accdate)

def filter_traffic(df):
    return df[(df['road_number'] == 1) | (df['road_number'] == 2) | (df['road_number'] == 7)]


def map_traffic_with_latlon(df):
    df['lat'] = df.apply(lambda row: df_km127[(df_km127['rd'] == row['road_number']) & (df_km127['km'] == row['km'])]['lat'].values[0]
                         if len(df_km127[(df_km127['rd'] == row['road_number']) & (df_km127['km'] == row['km'])]['lat'].values) > 0 else 0, axis=1)
    df['lon'] = df.apply(lambda row: df_km127[(df_km127['rd'] == row['road_number']) & (df_km127['km'] == row['km'])]['lon'].values[0]
                         if len(df_km127[(df_km127['rd'] == row['road_number']) & (df_km127['km'] == row['km'])]['lon'].values) > 0 else 0, axis=1)
    return df

def line_notify(lat, lon, date):
    headers = {
        'content-type':
            'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + LINE_TOKEN
    }
    # msg = input("Enter your name:")
    msg = date + " Accident at " + "Latitude : "+lat + ", Longitude : "+lon
    r = requests.post(LINE_URL, headers=headers, data={'message': msg})
    print(r.text)


def post_db(date, lat, lon):
    ref = db.reference('Accident')
    data = {
        'datetime': date,
        'coor': {
            'lat': lat,
            'lon': lon
        }
    }
    ref.push(data)

# schedule.every(2).seconds.do(csv_file)
schedule.every(1).minutes.do(csv_file)
# schedule.every(2).minutes.do(line_notify)
# schedule.every().hour.do(csv_file)
# schedule.every().day.at("10:30").do(csv_file)
# schedule.every(5).to(10).minutes.do(csv_file)
# schedule.every().monday.do(csv_file)
# schedule.every().wednesday.at("13:15").do(csv_file)
# schedule.every().minute.at(":17").do(csv_file)
while True:
    schedule.run_pending()
    time.sleep(1)
