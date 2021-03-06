import pandas as pd
import numpy as np
from datetime import datetime, date

def _filter_rows_by_values(df, column, keep_values):
    return df[df[column].isin(keep_values)]

class PreProcessRisk:
    
    @staticmethod
    def process_dataframe(dataset=None):
        
        if type(dataset) != pd.core.frame.DataFrame:
            dataset = pd.DataFrame()
            
        else:
            PreProcessRisk.dataset = dataset

        PreProcessRisk.dataset = PreProcessRisk.dataset.drop(columns=['Nederbord',
       'RH', 'Vindhastighet', 'Vindriktning', 'FFMC', 'DMC', 'DC', 'ISI',
       'BUI', 'HBV_o', 'HBV_u', 'HBV', 'HBV_index', 'Tmedel','Temp',
       'Gras','E','N'])
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
        pre2018risk = above4risk.loc['2000-1-1':'2017-12-31']
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
        return pre2018risk, pre2019risk, post2018risk,risk2000, risk2001, risk2002, risk2003, risk2004, risk2005, risk2006, risk2007, risk2008, risk2009, risk2010, risk2011, risk2012, risk2013, risk2014, risk2015, risk2016, risk2017, risk2018, risk2019, risk2020

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
        pre2018 = tablesplit.loc['2000-1-1':'2017-12-31']
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

        return pre2018, pre2019, post2018, fires2000, fires2001, fires2002, fires2003, fires2004, fires2005, fires2006, fires2007, fires2008, fires2009, fires2010, fires2011, fires2012, fires2013, fires2014, fires2015, fires2016, fires2017, fires2018, fires2019, fires2020

class PreProcessTables():
    @staticmethod
    def month_year(dataframe=None):
        month_year = pd.DataFrame(columns=['fires','Sum'])
        month_year['Month'] = dataframe['Month']
        month_year['Year'] = dataframe['Year']
        month_year['Date'] = dataframe['Date']
        month_year= month_year.assign(fires=1)
        month_year_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        month_year['Month_name'] = month_year['Month'].apply(lambda x: month_year_labels[x])
        month_year['Date'] = pd.to_datetime(month_year['Date'], format='%Y-%m-%d')
        month_year['yday'] = month_year['Date'].dt.dayofyear
        month_year['Day'] = month_year['Date'].dt.day
        month_year = month_year.sort_values(by=['Year','Month'])
        return month_year
    @staticmethod
    def fires_day_month(dataframe=None):
        dataframe = dataframe.reset_index()
        month_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        fires_day_month = pd.DataFrame(columns=['month_name','Sum'])
        fires_day_month['Sum'] = dataframe.value_counts(['Year','Day','Month']).to_frame()
        fires_day_month = fires_day_month.reset_index()
        fires_day_month['month_name'] = fires_day_month['Month'].apply(lambda x: month_labels[x])
        fires_day_month['Date'] = pd.to_datetime({'year':fires_day_month['Year'],'month': fires_day_month['Month'],'day':fires_day_month['Day']})
        fires_day_month['yday'] = fires_day_month['Date'].dt.dayofyear
        fires_day_month['Week'] = fires_day_month['Date'].dt.isocalendar().week
        return fires_day_month
    @staticmethod
    def fires_day_month_rol_mean(dataframe=None):
        tablesplit = dataframe.set_index(['Date'])
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
        fires_day_month_v2['rol5'] = fires_day_month_v2[['Date','Sum']].rolling(5).mean()
        fires_day_month_v2['rol14'] = fires_day_month_v2[['Date','Sum']].rolling(14).mean()
        fires_day_month_v2['rol7'] = fires_day_month_v2[['Date','Sum']].rolling(14).mean()
        return fires_day_month_v2
    @staticmethod
    def fire_muni(dataframe=None):
        dataframe['Municipality_name'] = dataframe['Municipality_name'].replace('Malung','Malung-Sälen')
        fire_muni = dataframe
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
        allyears = allyears.groupby(allyears['Municipality_name']).sum()
        allyears= allyears.reset_index()
        fire_muni_pre2019= fire_muni_pre2019.groupby(fire_muni_pre2019['Municipality_name']).sum()
        fire_muni_pre2019= fire_muni_pre2019.reset_index()
        fire_muni_post2018= fire_muni_post2018.groupby(fire_muni_post2018['Municipality_name']).sum()
        fire_muni_post2018= fire_muni_post2018.reset_index()
        return fire_muni_pre2019,fire_muni_post2018, allyears
