import schedule
import time
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

PATH = os.getenv('PATH-WEB')
df_km127 = pd.read_csv("./dataset/latlon_km127.csv")

def csv_file():
    header_list =  ['datetime','road_number','km','direction','all_units','inflow_units','outflow_unit','samecell_units','avg_speed','max_speed','avg_traveltime','max_traveltime']
    df = pd.read_csv(PATH,names=header_list,parse_dates=["datetime"])
    df_traffic = filter_traffic(df)
    print(df_traffic)
    # df_traffic_wlatlon = map_traffic_with_latlon(df_traffic)
    # print(df_traffic_wlatlon)

def filter_traffic(df):
    return df[(df['road_number']==1) | (df['road_number']==2) | (df['road_number']==7)]

def map_traffic_with_latlon(df):
    return df

# schedule.every(2).seconds.do(csv_file)
schedule.every(2).minutes.do(csv_file)
# schedule.every().hour.do(csv_file)
# schedule.every().day.at("10:30").do(csv_file)
# schedule.every(5).to(10).minutes.do(csv_file)
# schedule.every().monday.do(csv_file)
# schedule.every().wednesday.at("13:15").do(csv_file)
# schedule.every().minute.at(":17").do(csv_file)
csv_file()
# while True:
#     schedule.run_pending()
#     time.sleep(1)
