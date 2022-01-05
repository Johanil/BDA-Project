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
        risk2000 = above4risk.loc['2000-1-1' : '2000-12-31']
        risk2001 = above4risk.loc['2001-1-1' : '2001-12-31']
        risk2002 = above4risk.loc['2002-1-1' : '2002-12-31']
        risk2003 = above4risk.loc['2003-1-1' : '2003-12-31']
        risk2004 = above4risk.loc['2004-1-1' : '2004-12-31']
        risk2005 = above4risk.loc['2005-1-1' : '2005-12-31']
        risk2006 = above4risk.loc['2006-1-1' : '2006-12-31']
        risk2007 = above4risk.loc['2007-1-1' : '2007-12-31']
        risk2008 = above4risk.loc['2008-1-1' : '2008-12-31']
        risk2009 = above4risk.loc['2009-1-1' : '2009-12-31']
        risk2010 = above4risk.loc['2010-1-1' : '2010-12-31']
        risk2011 = above4risk.loc['2011-1-1' : '2011-12-31']
        risk2012 = above4risk.loc['2012-1-1' : '2012-12-31']
        risk2013 = above4risk.loc['2013-1-1' : '2013-12-31']
        risk2014 = above4risk.loc['2014-1-1' : '2014-12-31']
        risk2015 = above4risk.loc['2015-1-1' : '2015-12-31']
        risk2016 = above4risk.loc['2016-1-1' : '2016-12-31']
        risk2017 = above4risk.loc['2017-1-1' : '2017-12-31']
        risk2018 = above4risk.loc['2018-1-1' : '2018-12-31']
        risk2019 = above4risk.loc['2019-1-1' : '2019-12-31']
        risk2020 = above4risk.loc['2020-1-1' : '2029-12-31']
        return pre2019risk, post2018risk,risk2000, risk2001, risk2002, risk2003, risk2004, risk2005, risk2006, risk2007, risk2008, risk2009, risk2010, risk2011, risk2012, risk2013, risk2014, risk2015, risk2016, risk2017, risk2018, risk2019, risk2020

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
        fires2000 = tablesplit.loc['2000-1-1' : '2000-12-31']
        fires2001 = tablesplit.loc['2001-1-1' : '2001-12-31']
        fires2002 = tablesplit.loc['2002-1-1' : '2002-12-31']
        fires2003 = tablesplit.loc['2003-1-1' : '2003-12-31']
        fires2004 = tablesplit.loc['2004-1-1' : '2004-12-31']
        fires2005 = tablesplit.loc['2005-1-1' : '2005-12-31']
        fires2006 = tablesplit.loc['2006-1-1' : '2006-12-31']
        fires2007 = tablesplit.loc['2007-1-1' : '2007-12-31']
        fires2008 = tablesplit.loc['2008-1-1' : '2008-12-31']
        fires2009 = tablesplit.loc['2009-1-1' : '2009-12-31']
        fires2010 = tablesplit.loc['2010-1-1' : '2010-12-31']
        fires2011 = tablesplit.loc['2011-1-1' : '2011-12-31']
        fires2012 = tablesplit.loc['2012-1-1' : '2012-12-31']
        fires2013 = tablesplit.loc['2013-1-1' : '2013-12-31']
        fires2014 = tablesplit.loc['2014-1-1' : '2014-12-31']
        fires2015 = tablesplit.loc['2015-1-1' : '2015-12-31']
        fires2016 = tablesplit.loc['2016-1-1' : '2016-12-31']
        fires2017 = tablesplit.loc['2017-1-1' : '2017-12-31']
        fires2018 = tablesplit.loc['2018-1-1' : '2018-12-31']
        fires2019 = tablesplit.loc['2019-1-1' : '2019-12-31']
        fires2020 = tablesplit.loc['2020-1-1' : '2020-12-31']

        return pre2019, post2018, fires2000, fires2001, fires2002, fires2003, fires2004, fires2005, fires2006, fires2007, fires2008, fires2009, fires2010, fires2011, fires2012, fires2013, fires2014, fires2015, fires2016, fires2017, fires2018, fires2019, fires2020
