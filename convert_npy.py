from time import process_time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

temperature_file = "processed_data/total_temperature_4_years.csv"
irradiance_file = "processed_data/total_irradiance_4_years.csv"

def process_weather_csv(irradiance_file, temperature_file):
    # read files
    irradiance_df = pd.read_csv(irradiance_file)
    temperature_df = pd.read_csv(temperature_file)

    # process data to convert it to arrays
    irradiance_df['time'] = pd.to_datetime(irradiance_df['time'])
    irradiance_df['hour'] = irradiance_df['time'].dt.hour
    irradiance_df = irradiance_df.groupby(['season', 'hour'])['GHI'].mean().unstack()

    print(temperature_df)
    temperature_df['valid_time'] = pd.to_datetime(temperature_df['valid_time'])
    temperature_df['hour'] = temperature_df['valid_time'].dt.hour
    temperature_df = temperature_df.groupby(['season', 'hour'])['t2m'].mean().unstack()
    
    # conver to np as arrays
    irradiance_seasons = irradiance_df.to_numpy().T
    temperature_seasons = temperature_df.to_numpy().T

    np.save('processed_data/irradiance_seasons.npy', irradiance_seasons)
    np.save('processed_data/temperature_seasons.npy', temperature_seasons)

if __name__ == '__main__':
    process_weather_csv(irradiance_file, temperature_file)

