import cdsapi

#variables for position and resolution of data
dataset = "cams-solar-radiation-timeseries"
request = {
    "sky_type": "observed_cloud",
    "location": {"longitude": -1.6, "latitude": 56},
    "altitude": ["-999."],
    "date": ["2020-01-01/2023-12-31"],
    "time_step": "1hour",
    "time_reference": "universal_time",
    "format": "csv"
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()




#variables for position and resolution of data
dataset = 'reanalysis-era5-single-levels'
request = {
    'product_type': ['reanalysis'],
    'variable': ['2m_temperature'],
    'year': ['2020', '2021', '2022', '2023'],
    'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
    'day': 
        [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
    'time': 
        [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
    'area': [54.98, -1.62, 54.96, -1.58],
    'data_format': 'grib',
}
target = 'download.grib'

client.retrieve(dataset, request, target)


