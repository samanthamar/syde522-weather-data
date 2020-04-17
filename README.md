Usage: 
* Need to generate data month by month
* Edit python file to modify the date range and outfile csv file name 
* `python3 get_data.py` 

CSV Format: 
date, station1, avg_temp, windspeed_avg, precipitation_total, station_n, ...

Files with Missing Data:
* aug2018.csv (missing LAX and EWR)
* sept2019.csv (missing 1 data point for LAX) 
* oct2019.csv (missing lots of points for LAX)
* nov2019.csv (missing lots of points for LAX)