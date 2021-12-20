import pandas as pd
import numpy as np
import json
import logging
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.pyplot import xticks
from folium import plugins
from selenium import webdriver
from ipywidgets import interact, interactive, fixed, interact_manual
from IPython.display import display, clear_output


def main():
    path = Path(r"C:\BDA-Project\BDA-project\data\processed\FiresWithRisks 2000-2020.csv")
    df = pd.read_csv(path)
    print(df)
    plt.rcParams["figure.figsize"] = (18,8)
    month_year = pd.DataFrame(columns=['fires','Sum'])
   
    month_year['Month'] = df['Month']
    month_year['Year'] = df['Year']
    month_year['Date'] = df['Date']
    month_year= month_year.assign(fires=1)
    month_year_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    month_year['Month_name'] = month_year['Month'].apply(lambda x: month_year_labels[x])
    month_year['Date'] = pd.to_datetime(month_year['Date'], format='%Y-%m-%d')
    month_year['yday'] = month_year['Date'].dt.dayofyear
    month_year['Day'] = month_year['Date'].dt.day
    month_year = month_year.sort_values(by=['Year','Month'])
    logger = logging.getLogger(__name__)
    logger.info('Creating plots')
    print(df)
    create_fires_month_year_lineplot(month_year)
    df = df.reset_index()
    fires_day_month = pd.DataFrame(columns=['month_name','Sum'])
    fires_day_month['Sum'] = month_year.value_counts(['Year','yday','Day','Month']).to_frame()
    fires_day_month = fires_day_month.reset_index()
    month_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    fires_day_month['month_name'] = fires_day_month['Month'].apply(lambda x: month_labels[x])
    fires_day_month['Date'] = pd.to_datetime({'year':fires_day_month['Year'],'month': fires_day_month['Month'],'day':fires_day_month['Day']})
    tablesplit = fires_day_month.set_index(['Date'])
    pre2019 = tablesplit.loc['2000-1-1':'2018-12-31']
    pre2019['year_group'] = '2000-2018'
    post2018 = tablesplit.loc['2019-1-1' : '2020-12-31']
    post2018['year_group'] = '2019-2020 '
    post2018.sort_values(by='yday')
    fires_day_month_v2 = pd.concat([pre2019,post2018])
    fires_day_month_v2= fires_day_month_v2.reset_index()
    fires_day_month_v2 = fires_day_month_v2.sort_values(by='Date')
    fires_day_month_v2['rol7'] = fires_day_month_v2[['Date','Sum']].rolling(7).mean()
    create_fires_yday_lineplot(fires_day_month_v2)
    create_fires_yday_rol7_mean_grouped(fires_day_month_v2)

#Seems to be working, result needs to be double checked! Values only from april to august. Reasonable? All are FWI >=4
def create_fires_month_year_lineplot(df):
    month_labels = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    fig = df.groupby(['Month','Year']).sum().unstack()
    line = fig.plot(kind='line',y='fires', stacked=True)
    line.set_xticks([4,5,6,7,8,9,10])
    line.set_xticklabels(month_labels)
    line.legend(loc='center right')
    path = Path(r"C:\BDA-Project\BDA-project\reports\figures\fires_month_year_lineplot")
    plt.savefig(path)

def create_fires_yday_lineplot(df):

    fig = df.groupby(['yday','Year']).sum().unstack()
    line = fig.plot(kind='line',y='Sum', stacked=True)
    plt.xticks(np.linspace(0,365,13)[:-1], ('Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct', 'Nov', 'Dec'))
    #line.set_xticks(np.linspace(0,365,13)[:-1], ('Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct', 'Nov', 'Dec'))
    #line.set_xticklabels(fires_month['Month'].values)
    line.legend(loc='center right')
    path = Path(r"C:\BDA-Project\BDA-project\reports\figures\fires_yday_lineplot")
    plt.savefig(path)

def create_fires_yday_rol7_mean_grouped(df):
    fig = df.groupby(['yday','year_group']).median().unstack()
    line = fig.plot(kind='line',y='rol7', stacked=True)
    plt.xticks(np.linspace(0,365,13)[:-1], ('Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct', 'Nov', 'Dec'))
    line.legend(loc='center right')
    path = Path(r"C:\BDA-Project\BDA-project\reports\figures\fires_yday_rol7_mean_grouped")
    plt.savefig(path)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()