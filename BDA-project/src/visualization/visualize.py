import folium
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
import os
current_directory = os.getcwd()

def main():
    path = Path(current_directory+r"\BDA-project\data\processed\FiresWithRisks 2000-2020.csv")
    df = pd.read_csv(path)
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
    create_fires_month_year_lineplot(month_year)
    df = df.reset_index()
    fires_day_month = pd.DataFrame(columns=['month_name','Sum'])
    fires_day_month['Sum'] = month_year.value_counts(['Year','Day','Month']).to_frame()
    fires_day_month = fires_day_month.reset_index()
    month_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    fires_day_month['month_name'] = fires_day_month['Month'].apply(lambda x: month_labels[x])
    fires_day_month['Date'] = pd.to_datetime({'year':fires_day_month['Year'],'month': fires_day_month['Month'],'day':fires_day_month['Day']})
    fires_day_month['yday'] = fires_day_month['Date'].dt.dayofyear
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
    create_fires_yday_lineplot(fires_day_month_v2)
    create_fires_yday_rol7_mean_grouped(fires_day_month_v2)
    fire_muni = df
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
    allyears= allyears.groupby(allyears['Municipality_name']).sum()
    allyears= allyears.reset_index()
    fire_muni_pre2019= fire_muni_pre2019.groupby(fire_muni_pre2019['Municipality_name']).sum()
    fire_muni_pre2019= fire_muni_pre2019.reset_index()
    fire_muni_post2018= fire_muni_post2018.groupby(fire_muni_post2018['Municipality_name']).sum()
    fire_muni_post2018= fire_muni_post2018.reset_index()
    create_fires_muni_map(allyears)
    create_fires_muni_map(fire_muni_pre2019, "\muni_fire_pre2019.html")
    create_fires_muni_map(fire_muni_post2018,"\muni_fire_post2018.html")
 
#Seems to be working, result needs to be double checked! Values only from april to august. Reasonable? All are FWI >=4
def create_fires_month_year_lineplot(df):
    month_labels = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    fig = df.groupby(['Month','Year']).sum().unstack()
    line = fig.plot(kind='line',y='fires', stacked=True)
    line.set_xticks([4,5,6,7,8,9,10])
    line.set_xticklabels(month_labels)
    line.legend(loc='center right')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_month_year_lineplot")
    plt.savefig(path)

def create_fires_yday_lineplot(df):

    fig = df.groupby(['yday','Year']).sum().unstack()
    line = fig.plot(kind='line',y='Sum', stacked=True)
    plt.xticks(np.linspace(90,305,8)[:-1], ('Apr','May','Jun','Jul','Aug','Sep','Oct'))
    #line.set_xticks(np.linspace(0,365,13)[:-1], ('Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct', 'Nov', 'Dec'))
    #line.set_xticklabels(fires_month['Month'].values)
    line.legend(loc='center right')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_yday_lineplot")
    plt.savefig(path)

def create_fires_yday_rol7_mean_grouped(df):
    fig = df.groupby(['yday','year_group']).median().unstack()
    line = fig.plot(kind='line',y='rol7', stacked=True)
    plt.xticks(np.linspace(90,305,8)[:-1], ('Apr','May','Jun','Jul','Aug','Sep','Oct'))
    line.legend(loc='center right')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_yday_rol7_mean_grouped")
    plt.savefig(path)

def create_fires_muni_map(df, filename="muni_fire"):
    #df['Municipality_name'] = df['Municipality_name'].replace('Malung','Malung-Sälen')
    map = folium.Map(location = [59.334591, 18.063240],
               zoom_start = 5.45)

    path = Path(current_directory+r"\BDA-project\data\raw\sweden-municipalities-topo.json")
    with open(path,encoding='utf-8') as f:
        muni_topo = json.load(f)
    #Create Choropleth with data from allyears dataframe.
    folium.Choropleth(geo_data=muni_topo,
    topojson='objects.SWE_adm2',
    key_on='feature.properties.NAME_2',
    data=df, # What dataset to visualize
    columns=['Municipality_name','fires'], 
    fill_color='OrRd', 
    fill_opacity=0.9, 
    line_opacity=0.5,
    legend_name="Number of reported fires",
    threshold_scale=[1,2,4,8,16,32,64,128,256,512]
    ).add_to(map)
    fig_path = Path("\BDA-project\reports\figures")
    map.save(current_directory+r"\BDA-project\reports\figures"+filename)
    #map.save('./data/AllReportedFires.html')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()