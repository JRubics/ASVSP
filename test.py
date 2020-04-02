import pandas as pd
from urllib.error import HTTPError
from pathlib import Path

# Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
# Define the lat, long of the location and the year
# lat, lon, year = 34.05, -118.02, 2010
# You must request an NSRDB api key from the link above
api_key = 'KhSBYhiBiuDAclJcTxrDl3UlaCrvtGGA4b4vQoGX'
# Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
# attributes = 'air_temperature,dhi,dni,solar_zenith_angle'
attributes = 'air_temperature,dhi,dni,ghi,solar_zenith_angle,clearsky_dhi,clearsky_dni,cloud_type,relative_humidity'
# Choose year of data
year = '2018'
# Set leap year to true or false. True will return leap day data if present, false will not.
leap_year = 'false'
# Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
interval = '30'
# Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
# NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
# local time zone.
utc = 'false'
# Your full name, use '+' instead of spaces.
your_name = 'Jelena+Dokic'
# Your reason for using the NSRDB.
reason_for_use = 'education'
# Your affiliation
your_affiliation = 'ftn'
# Your email address
your_email = 'jelena.dpk@gmail.com'
# Please join our mailing list so we can keep you up-to-date on new developments.
mailing_list = 'false'

# //lat 90
# for lat in range(0, 30, 1):
#   for lon in range(-110, -70, 1):
for lat in [0]:
  for lon in [-71]:
    for year in [2015]:
      my_file = Path('dataset1/dataset_' + str(lat) + "_" + str(lon) + '_' + str(year) + '.csv')
      if not my_file.exists():
        try:
          df = pd.read_csv('http://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes), skiprows=2)

          df = df.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=interval + 'Min', periods=525600 / int(interval)))
          df.to_csv('datasetTest/dataset_' + str(lat) + "_" + str(lon) + '_' + str(year) + '.csv', sep='\t')
        except HTTPError as e:
          print("ERROR", lat, lon, e)
