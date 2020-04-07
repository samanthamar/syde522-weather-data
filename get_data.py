import dotenv 
import os
import requests
import pprint
import csv 

# Load api key 
dotenv.load_dotenv()
api_key = os.getenv('API_KEY')

# NOTE: would probably want a list of these 
station_id = 'KCAOAKLA44' # LA 
date = '20181001'

# Endpoint 
url = f'https://api.weather.com/v2/pws/history/daily?stationId={station_id}&format=json&units=m&date={date}&apiKey={api_key}'

# Make the request, get the json 
r = requests.get(url)
data = r.json()
pprint.pprint(data)

# Parse the revelevant data 
metric_data = data['observations'][0]['metric']
tempAvg = metric_data['tempAvg']
windspeedAvg = metric_data['windspeedAvg']
precipTotal = metric_data['precipTotal']

# Write the data to csv 
f = open('historical_data.csv', 'w')

with f:
    writer = csv.writer(f)
    # write the header 
    writer.writerow(['station_id', 'date', 'tempAvg', 'windspeedAvg', 'precipTotal'])
    # write the data
    writer.writerow([station_id, date, tempAvg, windspeedAvg, precipTotal])