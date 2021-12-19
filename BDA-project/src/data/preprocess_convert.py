import pandas as pd
from sweref99 import projections

class preprocess_converters():

    def __init__(self):
        self.tm = projections.make_transverse_mercator("SWEREF_99_TM")


    #Function for converting easting and northing to latitudes.
    #Exampl: sample['Latitude'] = sample.apply(lambda row: toLat(row['sweref99Ost'],row['sweref99Norr']),axis=1)
    @staticmethod
    def _convert_to_lat(df,E,N):
        lat, lon = df.tm.grid_to_geodetic(N,E)
        return lat

        #Function for converting easting and northing to longitude.
        #Exampl: sample['Longitude'] = sample.apply(lambda row: toLon(row['sweref99Ost'],row['sweref99Norr']),axis=1)
    @staticmethod
    def _convert_to_lon(df,E,N):
        lat, lon = df.tm.grid_to_geodetic(N,E)
        return lon
    @staticmethod
    def _convert_swereff99_column(df, column):
        return df

    @staticmethod
    def _convert_columns_totype(df,columns,type):
        for column in columns:
            df[column] = df[column].astype(type)
        return df
