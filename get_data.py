import dotenv 
import os
import requests
import pprint
import csv 
import pandas as pd 
from datetime import datetime

# Load api key 
dotenv.load_dotenv()
api_key = os.getenv('API_KEY')

# NOTE: would probably want a list of these 
# station_id = 'KCAOAKLA44' #LAX 
# station_id = 'KNJELIZA13' # EWR
# station_id =  'KNYQUEEN31' # JFK
# date = '20181001'

def generate_dates():
    # Change these dates 
    start = datetime(2018,8,1).strftime('%Y%m%d') 
    end = datetime(2018,8,31)
    pd_dates = pd.date_range(start, end).tolist()
    # Convert to proper format 
    dates = []
    for date in pd_dates:
        dates.append(date.strftime('%Y%m%d'))
    return dates 

# Get the date ranges for the data we want 
dates = generate_dates()

# List of the station ids we want the historical weather for 
# LAX, EWR, JFK 
station_ids = ['KCAOAKLA44', 'KNJELIZA13', 'KNYQUEEN31']
# Map the ids to airport code
airport = {
    'KCAOAKLA44': 'LAX',
    'KNJELIZA13': 'EWR', 
    'KNYQUEEN31': 'JFK'
}

def get_weather(station_id, date): 
    # Endpoint 
    url = f'https://api.weather.com/v2/pws/history/daily?stationId={station_id}&format=json&units=m&date={date}&apiKey={api_key}'

    # Make the request, get the json 
    r = requests.get(url)
    data = r.json()
    # pprint.pprint(data)

    # Parse the revelevant data 
    metric_data = data['observations'][0]['metric']
    tempAvg = metric_data['tempAvg']
    windspeedAvg = metric_data['windspeedAvg']
    precipTotal = metric_data['precipTotal']
    data = {
            'avg_temp': tempAvg, 
            'windspeed_avg': windspeedAvg, 
            'precipitation': precipTotal
        }
    return data 

weather_data = {}
for date in dates: 
    print(date)
    weather_at_stations = []
    for station in station_ids: 
        print(station)
        weather = {}
        try:
            weather[station] = get_weather(station, date)
        except:
            continue 
        weather_at_stations.append(weather)
    weather_data[date] = weather_at_stations

# pprint.pprint(weather_data)

# Export to csv 
# Write the data to csv 
# File name changes...need to do it month by month
f = open('aug2018.csv', 'w')

with f:
    writer = csv.writer(f)
    # date, stationid, temp, windspeed, precipitation 
    # Parse out the data to write to row 
    for date in dates: 
        station_data = weather_data[date]
        data = []
        data.append(date)
        for station in station_data:
            for k,v in station.items():
                print(k,v)   
                data.append(airport[k])
                data.append(v['avg_temp'])         
                data.append(v['windspeed_avg'])
                data.append(v['precipitation'])
        writer.writerow(data)
        
# # Endpoint 
# url = f'https://api.weather.com/v2/pws/history/daily?stationId={station_id}&format=json&units=m&date={date}&apiKey={api_key}'

# # Make the request, get the json 
# r = requests.get(url)
# data = r.json()
# pprint.pprint(data)

# # Parse the revelevant data 
# metric_data = data['observations'][0]['metric']
# tempAvg = metric_data['tempAvg']
# windspeedAvg = metric_data['windspeedAvg']
# precipTotal = metric_data['precipTotal']

# # Write the data to csv 
# f = open('historical_data.csv', 'w')

# with f:
#     writer = csv.writer(f)
#     # write the header 
#     writer.writerow(['station_id', 'date', 'tempAvg', 'windspeedAvg', 'precipTotal'])
#     # write the data
#     writer.writerow([station_id, date, tempAvg, windspeedAvg, precipTotal])