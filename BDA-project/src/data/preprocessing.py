import pandas as pd
from sweref99 import projections

class PreProcess():
    
    df = pd.Dataframe
    tm = projections.make_transverse_mercator("SWEREF_99_TM")
    #def main(input_filepath):
        
    #Function which sums up the values of the columns into a new column and returns the dataframe
    def sum_columns(df, columns, new_column_name):
        df[new_column_name] = df[columns].sum(axis=1)

        return df

    def sum_columns(df, columns, new_column_name):
        df[new_column_name] = df[columns].sum(axis=1)

        return df

    def filter_rows_by_values(df, column, keep_values):
        #Replace ~ with - try if it works
        return df[df[column].isin(keep_values)]

    def print_null_values(df):
        for column in df:
            if df[column].isnull().any():
                print('{0} has {1} null values'.format(column, df[column].isnull().sum()))

    def print_column_missing_values(df,column):
        x = len(df)
        if df[column].isnull().any():
            print('{0} has total of {1} null values'.format(column, df[column].isnull().sum()))
            print ('In the column {0}'.format(column), round(100-(df[column].count()/x * 100), 3), '% of the cells have missing values')
    
        #Functions for converting easting and northing to latitudes and longitudes.
        #Exampl: sample['Latitude'] = sample.apply(lambda row: toLat(row['sweref99Ost'],row['sweref99Norr']),axis=1)
    def convert_to_lat(E,N):
        lat, lon = tm.grid_to_geodetic(N,E)
        return lat

    def convert_to_lon(E,N):
        lat, lon = tm.grid_to_geodetic(N,E)
        return lon

    def convert_swereff99_column(df, column):
        return df


    def convert_columns_totype(df,columns,type):
        for column in columns:
            df[column] = df[column].astype(type)
        return df

    def column_value_replace(df,columns,to_replace,replace_with):
        for column in columns:
            df[column] = df[column].str.replace(to_replace,replace_with)
        return df

    def format_date_column(df,column,format_value):
        df[column] = pd.to_datetime(df[column], format=format_value)


    