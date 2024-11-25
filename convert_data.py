import xarray as xr
import pandas as pd
import datetime

kelvin_temperature = 273.15
date_period = '2020-01-01/2023-01-31'

#Clean temperature data ready to process 
# Load xarray dataset from a file
file_path = 'raw_data/download.grib'
xarray_dataset = xr.open_dataset(file_path)
# Convert xarray dataset to pandas DataFrame
df = xarray_dataset.to_dataframe()
df = df.set_index(df['valid_time'])
df = df['t2m'] - kelvin_temperature
# df = df.resample('T').interpolate()
if "/" in date_period:
    range_days = date_period.split('/')
    mask = (df.index >= range_days[0]) & (df.index <= range_days[1])
    df.loc[mask].to_csv("processed_data/temperature.csv")

else:
    df.loc[date_period].to_csv("processed_data/temperature.csv")

#Clean data from irradiation ready to process
with open('raw_data/irradiation.csv', newline='') as weather_data:
    irradiance = pd.read_csv(weather_data, skiprows=42, delimiter=';')
    irradiance.rename(columns={irradiance.columns[0]: irradiance.columns[0].lstrip('# ')}, inplace=True)
    irradiance['index_date'] = irradiance['Observation period'].apply(lambda x: x.split('/')[0])
    irradiance['index_date'] = pd.to_datetime(irradiance['index_date'])
    irradiance.set_index(irradiance['index_date'], inplace=True)
    irradiance = irradiance[['DHI', 'GHI']]

irradiance.to_csv('processed_data/irradiance.csv')
