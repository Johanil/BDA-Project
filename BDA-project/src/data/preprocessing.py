import pandas as pd
import numpy as np
from datetime import datetime, date
from sweref99 import projections
from preprocess_convert import preprocess_converters
#from preprocess_convert import preprocess_convert

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
        return pre2019risk, post2018risk

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

        return pre2019, post2018
