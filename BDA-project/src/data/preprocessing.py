import pandas as pd
import numpy as np
import os
from datetime import datetime, date
from sweref99 import projections
from pathlib import Path
from preprocess_convert import preprocess_converters
current_directory = os.getcwd()

def _filter_rows_by_values(df, column, keep_values):
    return df[df[column].isin(keep_values)]

def _sum_columns(df, columns, new_column_name):
    df[new_column_name] = df[columns].sum(axis=1)
    return df



class PreProcessRisk:
    
    @staticmethod
    def process_dataframe(dataset=None):
        
        if type(dataset) != pd.core.frame.DataFrame:
            dataset = pd.DataFrame()
            
        else:
            PreProcessRisk.dataset = dataset

        # Initializing instances of the smaller profile DF and the larger DF
        PreProcessRisk.dataset = PreProcessRisk.dataset.drop(columns=['Nederbord',
       'RH', 'Vindhastighet', 'Vindriktning', 'FFMC', 'DMC', 'DC', 'ISI',
       'BUI', 'HBV_o', 'HBV_u', 'HBV', 'HBV_index', 'Tmedel','Temp',
       'Gras','E','N'])
        tm = projections.make_transverse_mercator("SWEREF_99_TM")
        pc = preprocess_converters()
        PreProcessRisk.dataset.dropna(subset=['FWI'], how='all', inplace=True)
        PreProcessRisk.dataset['FWI'] = PreProcessRisk.dataset['FWI'].str.replace(',','.')
        PreProcessRisk.dataset['FWI'] = PreProcessRisk.dataset['FWI'].astype(float)
        PreProcessRisk.dataset['Kommun'] = PreProcessRisk.dataset['Kommun'].astype(int)
        PreProcessRisk.dataset['Datum'] = pd.to_datetime(PreProcessRisk.dataset['Datum'], format='%Y-%m-%d')
        PreProcessRisk.dataset = PreProcessRisk.dataset.groupby(['Datum','Kommun']).mean()
        PreProcessRisk.dataset = PreProcessRisk.dataset.reset_index()
        PreProcessRisk.dataset = PreProcessRisk.dataset.rename(columns={"Datum": "Date", "Kommun":"Municipality"})
        return PreProcessRisk.dataset

    @staticmethod
    def process_dataframe_fwi4_days(df):
        
        #Creates table from the firerisktable grouped on the columns Datum and Kommun, with the median, giving us the median values of FWI_index for each Kommun and each day
        totalfwi4 = df.groupby(['Date','Municipality']).median()
        totalfwi4 = df.reset_index()
        # Gives us table with for all the times FWI_index was => 4 (eldningsförbud)
        above4risk = totalfwi4[totalfwi4['FWI_index']>=4]
        above4risk = above4risk.set_index(['Date'])
        pre2019risk = above4risk.loc['2000-1-1':'2018-12-31']
        post2018risk = above4risk.loc['2019-1-1' : '2020-12-31']
        risk2018 = above4risk.loc['2018-1-1' : '2018-12-31']
        risk2019 = above4risk.loc['2019-1-1' : '2019-12-31']
        risk2020 = above4risk.loc['2020-1-1' : '2029-12-31']
        return pre2019risk, post2018risk, risk2018, risk2019, risk2020

    @staticmethod
    def _sum_columns(dataset, columns, new_column_name):
        dataset[new_column_name] = dataset[columns].sum(axis=1)

        return dataset
    @staticmethod
    def _column_value_replace(dataset,columns,to_replace,replace_with):
        for column in columns:
            dataset[column] = dataset[column].str.replace(to_replace,replace_with)
        return dataset
    @staticmethod
    def _format_date_column(dataset,column,format_value):
        dataset[column] = pd.to_datetime(dataset[column], format=format_value)

class PreProcessReported():
    @staticmethod
    def process_dataframe(dataset):
        if type(dataset) != pd.core.frame.DataFrame:
            dataset = pd.DataFrame()
        else:
            dataset = dataset
        dataset = _filter_rows_by_values(dataset,'BEJBbrandorsakText',['Grillning eller lägereld'])
        dataset = _sum_columns(dataset,['arealProduktivSkogsmark_m2','arealAnnanTradbevuxenMark_m2','arealMarkUtanTrad_m2'],'TotArea')
        dataset['Hectares'] = dataset['TotArea']/10000
        dataset = dataset.drop(columns=['tid','sweref99Ost','sweref99Norr','verksamhetText','arealProduktivSkogsmark_m2','arealAnnanTradbevuxenMark_m2','arealMarkUtanTrad_m2','BEJBbrandorsakText'])
        dataset['Month'] = dataset['datum'].dt.month
        dataset['Day'] = dataset['datum'].dt.day
        dataset = dataset.rename(columns={"datum":"Date", "kommun":"Municipality"})
        return dataset

    
class PreProcessMerge():

    @staticmethod
    def process_dataframe(risk_dataset=None, fires_dataset=None, fwi_filter=-1):
            # Initializing instances of the smaller profile DF and the larger DF
        if type(fires_dataset) != pd.core.frame.DataFrame:
            fires_dataset = pd.DataFrame()
        else:
            fires_dataset = fires_dataset
        if type(risk_dataset) != pd.core.frame.DataFrame:
            risk_dataset = pd.DataFrame() 
        else:
            risk_dataset = risk_dataset

        df = pd.merge(fires_dataset, risk_dataset, how='inner', on=['Municipality','Date'])
        df = df.rename(columns={ "datum":"Date", "kommun":"Municipality_name","BEJBbrandorsakText":"Cause_of_fire","kommunKortNamn":"Municipality_name","ar":"Year"})
        
        df = df[df['FWI_index']>=fwi_filter]
        return df

    @staticmethod
    def process_dataframe_fwi4_days(dataset=None):
        dataset['Date'] = pd.to_datetime({'year':dataset['Year'],'month': dataset['Month'],'day':dataset['Day']})
        tablesplit = dataset.set_index(['Date'])
        pre2019 = tablesplit.loc['2000-1-1':'2018-12-31']
        post2018 = tablesplit.loc['2019-1-1' : '2020-12-31']
        fires2018 = tablesplit.loc['2018-1-1' : '2018-12-31']
        fires2019 = tablesplit.loc['2019-1-1' : '2019-12-31']
        fires2020 = tablesplit.loc['2020-1-1' : '2020-12-31']

        return pre2019, post2018, fires2018, fires2019, fires2020

class PreProcessFigures():
    @staticmethod
    def make__month_year_lineplot_csv(dataset=None):
        path = Path(current_directory+r"\BDA-project\data\processed\FiresWithRisks 2000-2020.csv")
        dataset = pd.read_csv(path)
        month_year = pd.DataFrame(columns=['fires','Sum'])
        month_year['Month'] = dataset['Month']
        month_year['Year'] = dataset['Year']
        month_year['Date'] = dataset['Date']
        month_year= month_year.assign(fires=1)
        month_year_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        month_year['Month_name'] = month_year['Month'].apply(lambda x: month_year_labels[x])
        month_year['Date'] = pd.to_datetime(month_year['Date'], format='%Y-%m-%d')
        month_year['yday'] = month_year['Date'].dt.dayofyear
        month_year['Day'] = month_year['Date'].dt.day
        month_year = month_year.sort_values(by=['Year','Month'])

    def make_line_plot_csv(dataset=None):
        path = Path(current_directory+r"\BDA-project\data\processed\FiresWithRisks 2000-2020.csv")
        dataset = pd.read_csv(path)
        month_year = pd.DataFrame(columns=['fires','Sum'])
        month_year['Month'] = dataset['Month']
        month_year['Year'] = dataset['Year']
        month_year['Date'] = dataset['Date']
        month_year= month_year.assign(fires=1)
        month_year_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        month_year['Month_name'] = month_year['Month'].apply(lambda x: month_year_labels[x])
        month_year['Date'] = pd.to_datetime(month_year['Date'], format='%Y-%m-%d')
        month_year['yday'] = month_year['Date'].dt.dayofyear
        month_year['Day'] = month_year['Date'].dt.day
        month_year = month_year.sort_values(by=['Year','Month'])
        dataset = dataset.reset_index()
        fires_day_month = pd.DataFrame(columns=['month_name','Sum'])
        fires_day_month['Sum'] = month_year.value_counts(['Year','Day','Month']).to_frame()
        fires_day_month = fires_day_month.reset_index()
        month_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        fires_day_month['month_name'] = fires_day_month['Month'].apply(lambda x: month_labels[x])
        fires_day_month['Date'] = pd.to_datetime({'year':fires_day_month['Year'],'month': fires_day_month['Month'],'day':fires_day_month['Day']})
        fires_day_month['yday'] = fires_day_month['Date'].dt.dayofyear
        fires_day_month['Week'] = fires_day_month['Date'].dt.week
        tablesplit = fires_day_month.set_index(['Date'])
        #FutureWarning at this row
        pre2019 = tablesplit.loc['2000-1-1':'2018-12-31']
        #FutureWarning at this row
        pre2019['year_group'] = '2000-2018'
        post2018 = tablesplit.loc['2019-1-1' : '2020-12-31']
        post2018['year_group'] = '2019-2020 '
        post2018.sort_values(by='yday')
        fires_day_month_v2 = pd.concat([pre2019,post2018])
        fires_day_month_v2= fires_day_month_v2.reset_index()
        fires_day_month_v2 = fires_day_month_v2.sort_values(by='Date')
        fires_day_month_v2['rol7'] = fires_day_month_v2[['Date','Sum']].rolling(14).mean()

    def make_clo_map_csv(dataset=None):
        fire_muni = dataset
        fire_muni = fire_muni[['Date','Municipality_name']]
        allyears = pd.DataFrame(columns=['fires'])
        fire_muni_pre2019 = pd.DataFrame(columns=['fires'])
        fire_muni_post2018 = pd.DataFrame(columns=['fires'])
        tt = fire_muni.set_index(['Date'])
        fire_muni_pre2019 = tt.loc['2000-01-01':'2018-12-31']
        fire_muni_pre2019['year_group'] = '2000-2018'
        fire_muni_post2018 = tt.loc['2019-01-01' : '2020-12-31']
        fire_muni_post2018['year_group'] = '2019-2020'
        fire_muni_post2018.sort_values(by='Date')
        allyears = pd.concat([fire_muni_pre2019,fire_muni_post2018])
        allyears = allyears.assign(fires=1)
        fire_muni_pre2019 = fire_muni_pre2019.assign(fires=1)
        fire_muni_post2018 = fire_muni_post2018.assign(fires=1)
        allyears['Municipality_name'] = allyears['Municipality_name'].replace('Malung','Malung-Sälen')
        allyears = allyears.groupby(allyears['Municipality_name']).sum()
        allyears= allyears.reset_index()
        fire_muni_pre2019= fire_muni_pre2019.groupby(fire_muni_pre2019['Municipality_name']).sum()
        fire_muni_pre2019= fire_muni_pre2019.reset_index()
        fire_muni_post2018= fire_muni_post2018.groupby(fire_muni_post2018['Municipality_name']).sum()
        fire_muni_post2018= fire_muni_post2018.reset_index()