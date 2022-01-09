from typing import Container
import folium
from jinja2.bccache import Bucket
import pandas as pd
import numpy as np
import json
import logging
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.pyplot import xticks
import matplotlib.transforms
from folium import plugins
from selenium import webdriver
from ipywidgets import interact, interactive, fixed, interact_manual
from IPython.display import display, clear_output
from pandas.plotting import table 
import os
current_directory = os.getcwd()

def main():
    month_year_path = Path(current_directory+r"\BDA-project\data\processed\month_year.csv")
    fires_day_month_rol_mean_path = Path(current_directory+r"\BDA-project\data\processed\fires_day_month_rol_mean.csv")
    fire_muni_pre2019_path = Path(current_directory+r"\BDA-project\data\processed\fire_muni_pre2019.csv")
    fire_muni_post2018_path = Path(current_directory+r"\BDA-project\data\processed\fire_muni_post2018.csv")
    allyears_path = Path(current_directory+r"\BDA-project\data\processed\allyears.csv")
    month_year = pd.read_csv(month_year_path)
    fires_day_month_rol_mean = pd.read_csv(fires_day_month_rol_mean_path)
    fire_muni_post2018 = pd.read_csv(fire_muni_post2018_path)
    fire_muni_pre2019 = pd.read_csv(fire_muni_pre2019_path)
    allyears = pd.read_csv(allyears_path)
    plt.rcParams["figure.figsize"] = (18,8)

    logger = logging.getLogger(__name__)
    logger.info('Creating plots')
    create_fires_month_year_lineplot(month_year)

    create_fires_yday_lineplot(fires_day_month_rol_mean)
    create_fires_week_lineplot(fires_day_month_rol_mean)
    create_fires_yday_rol5_mean_grouped(fires_day_month_rol_mean)
    create_fires_yday_rol7_mean_grouped(fires_day_month_rol_mean)
    create_fires_yday_rol14_mean_grouped(fires_day_month_rol_mean)


    create_fires_muni_map(allyears,r"\allyears.html")
    create_fires_muni_map(fire_muni_pre2019, "\muni_fire_pre2019.html")
    create_fires_muni_map(fire_muni_post2018,"\muni_fire_post2018.html")
    
    fires_per_fwi4()
    logger.info('Plots created')

#Seems to be working, result needs to be double checked! Values only from april to august. Reasonable? All are FWI >=4
def create_fires_month_year_lineplot(df):
    month_labels = ['Jan','Feb','Mar','Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct','Nov','Dec']
    fig = df.groupby(['Month','Year']).sum().unstack()
    line = fig.plot(kind='line',y='fires', stacked=True)
    line.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
    line.set_xticklabels(month_labels)
    line.legend(loc='center right')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_month_year_lineplot")
    plt.savefig(path)

def create_fires_yday_lineplot(df):

    fig = df.groupby(['yday','Year']).sum().unstack()
    line = fig.plot(kind='line',y='Sum', stacked=True)
    #plt.xticks(np.linspace(90,305,8)[:-1], ('Apr','May','Jun','Jul','Aug','Sep','Oct'))
    #line.set_xticks(np.linspace(0,365,13)[:-1], ('Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct', 'Nov', 'Dec'))
    #line.set_xticklabels(fires_month['Month'].values)
    line.legend(loc='center right')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_yday_lineplot")
    plt.savefig(path)

def create_fires_week_lineplot(df):
    
    fig = df.groupby(['Week','Year']).sum().unstack()
    line = fig.plot(kind='line',y='Sum', stacked=True)
    #plt.xticks(np.linspace(0,52,53)[:-1])#, ('Apr','May','Jun','Jul','Aug','Sep','Oct'))
    #line.set_xticks(np.linspace(0,365,13)[:-1], ('Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct', 'Nov', 'Dec'))
    #line.set_xticklabels(fires_month['Month'].values)
    line.legend(loc='center right')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_week_lineplot")
    plt.savefig(path)

def create_fires_yday_rol7_mean_grouped(df):
    fig = df.groupby(['Week','year_group']).median().unstack()
    line = fig.plot(kind='line',y='rol7', stacked=True)
    #plt.xticks(np.linspace(90,305,8)[:-1], ('Apr','May','Jun','Jul','Aug','Sep','Oct'))
    line.legend(loc='center right')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_yday_rol7_mean_grouped")
    plt.savefig(path)

def create_fires_yday_rol14_mean_grouped(df):
    fig = df.groupby(['Week','year_group']).median().unstack()
    line = fig.plot(kind='line',y='rol14', stacked=True)
    #plt.xticks(np.linspace(90,305,8)[:-1], ('Apr','May','Jun','Jul','Aug','Sep','Oct'))
    line.legend(loc='center right')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_yday_rol14_mean_grouped")
    plt.savefig(path)

def create_fires_yday_rol5_mean_grouped(df):
    fig = df.groupby(['Week','year_group']).median().unstack()
    line = fig.plot(kind='line',y='rol5', stacked=True)
    #plt.xticks(np.linspace(4,10,8)[:-1], ('Apr','May','Jun','Jul','Aug','Sep','Oct'))
    line.legend(loc='center right')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_yday_rol5_mean_grouped")
    plt.savefig(path)

def create_fires_muni_map(df, filename="muni_fire"):
    map = folium.Map(location = [59.334591, 18.063240],
               zoom_start = 5.45)
    path = Path(current_directory+r"\BDA-project\data\raw\sweden-municipalities-topo.json")
    with open(path,encoding='utf-8') as f:
        muni_topo = json.load(f)

    pd.set_option('display.max_rows', df.shape[0]+1)
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
    ).add_to(map)
    map.save(current_directory+r"\BDA-project\reports\figures"+filename)
    #map.save('./data/AllReportedFires.html')
    path = Path(current_directory+r"\BDA-project\reports\figures\fires_yday_rol14_mean_grouped")
    plt.savefig(path)

def fires_per_fwi4():
    pre18riskPath = Path(current_directory+r"\BDA-project\data\processed\pre18fwi4Risk.csv")
    pre18risk= pd.read_csv(pre18riskPath)
    pre19riskPath = Path(current_directory+r"\BDA-project\data\processed\pre19fwi4Risk.csv")
    pre_risk= pd.read_csv(pre19riskPath)
    post18riskPath= Path(current_directory+r"\BDA-project\data\processed\post18fwi4Risk.csv")
    post_risk= pd.read_csv(post18riskPath)
    pre18mergedPath= Path(current_directory+r"\BDA-project\data\processed\pre18fwi4Merged.csv")
    pre18merged= pd.read_csv(pre18mergedPath)
    pre19mergedPath= Path(current_directory+r"\BDA-project\data\processed\pre19fwi4Merged.csv")
    pre_merged= pd.read_csv(pre19mergedPath)
    post18mergedPath= Path(current_directory+r"\BDA-project\data\processed\post18fwi4Merged.csv")
    post_merged= pd.read_csv(post18mergedPath)
    risk2000Path = Path(current_directory+r"\BDA-project\data\processed\risk2000.csv")
    risk00= pd.read_csv(risk2000Path)
    risk2001Path = Path(current_directory+r"\BDA-project\data\processed\risk2001.csv")
    risk01= pd.read_csv(risk2001Path)
    risk2002Path = Path(current_directory+r"\BDA-project\data\processed\risk2002.csv")
    risk02= pd.read_csv(risk2002Path)
    risk2003Path = Path(current_directory+r"\BDA-project\data\processed\risk2003.csv")
    risk03= pd.read_csv(risk2003Path)
    risk2004Path = Path(current_directory+r"\BDA-project\data\processed\risk2004.csv")
    risk04= pd.read_csv(risk2004Path)
    risk2005Path = Path(current_directory+r"\BDA-project\data\processed\risk2005.csv")
    risk05= pd.read_csv(risk2005Path)
    risk2006Path = Path(current_directory+r"\BDA-project\data\processed\risk2006.csv")
    risk06= pd.read_csv(risk2006Path)
    risk2007Path = Path(current_directory+r"\BDA-project\data\processed\risk2007.csv")
    risk07= pd.read_csv(risk2007Path)
    risk2008Path = Path(current_directory+r"\BDA-project\data\processed\risk2008.csv")
    risk08= pd.read_csv(risk2008Path)
    risk2009Path = Path(current_directory+r"\BDA-project\data\processed\risk2009.csv")
    risk09= pd.read_csv(risk2009Path)
    risk2010Path = Path(current_directory+r"\BDA-project\data\processed\risk2010.csv")
    risk10= pd.read_csv(risk2010Path)
    risk2011Path = Path(current_directory+r"\BDA-project\data\processed\risk2011.csv")
    risk11= pd.read_csv(risk2011Path)
    risk2012Path = Path(current_directory+r"\BDA-project\data\processed\risk2012.csv")
    risk12= pd.read_csv(risk2012Path)
    risk2013Path = Path(current_directory+r"\BDA-project\data\processed\risk2013.csv")
    risk13= pd.read_csv(risk2013Path)
    risk2014Path = Path(current_directory+r"\BDA-project\data\processed\risk2014.csv")
    risk14= pd.read_csv(risk2014Path)
    risk2015Path = Path(current_directory+r"\BDA-project\data\processed\risk2015.csv")
    risk15= pd.read_csv(risk2015Path)
    risk2016Path = Path(current_directory+r"\BDA-project\data\processed\risk2016.csv")
    risk16= pd.read_csv(risk2016Path)
    risk2017Path = Path(current_directory+r"\BDA-project\data\processed\risk2017.csv")
    risk17= pd.read_csv(risk2017Path)
    risk2018Path = Path(current_directory+r"\BDA-project\data\processed\risk2018.csv")
    risk18= pd.read_csv(risk2018Path)
    risk2019Path = Path(current_directory+r"\BDA-project\data\processed\risk2019.csv")
    risk19= pd.read_csv(risk2019Path)
    risk2020Path = Path(current_directory+r"\BDA-project\data\processed\risk2020.csv")
    risk20= pd.read_csv(risk2020Path)
    merged2000Path= Path(current_directory+r"\BDA-project\data\processed\2000merged.csv")
    merged00= pd.read_csv(merged2000Path)
    merged2001Path= Path(current_directory+r"\BDA-project\data\processed\2001merged.csv")
    merged01= pd.read_csv(merged2001Path)
    merged2002Path= Path(current_directory+r"\BDA-project\data\processed\2002merged.csv")
    merged02= pd.read_csv(merged2002Path)
    merged2003Path= Path(current_directory+r"\BDA-project\data\processed\2003merged.csv")
    merged03= pd.read_csv(merged2003Path)
    merged2004Path= Path(current_directory+r"\BDA-project\data\processed\2004merged.csv")
    merged04= pd.read_csv(merged2004Path)
    merged2005Path= Path(current_directory+r"\BDA-project\data\processed\2005merged.csv")
    merged05= pd.read_csv(merged2005Path)
    merged2006Path= Path(current_directory+r"\BDA-project\data\processed\2006merged.csv")
    merged06= pd.read_csv(merged2006Path)
    merged2007Path= Path(current_directory+r"\BDA-project\data\processed\2007merged.csv")
    merged07= pd.read_csv(merged2007Path)
    merged2008Path= Path(current_directory+r"\BDA-project\data\processed\2008merged.csv")
    merged08= pd.read_csv(merged2008Path)
    merged2009Path= Path(current_directory+r"\BDA-project\data\processed\2009merged.csv")
    merged09= pd.read_csv(merged2009Path)
    merged2010Path= Path(current_directory+r"\BDA-project\data\processed\2010merged.csv")
    merged10= pd.read_csv(merged2010Path)
    merged2011Path= Path(current_directory+r"\BDA-project\data\processed\2011merged.csv")
    merged11= pd.read_csv(merged2011Path)
    merged2012Path= Path(current_directory+r"\BDA-project\data\processed\2012merged.csv")
    merged12= pd.read_csv(merged2012Path)
    merged2013Path= Path(current_directory+r"\BDA-project\data\processed\2013merged.csv")
    merged13= pd.read_csv(merged2013Path)
    merged2014Path= Path(current_directory+r"\BDA-project\data\processed\2014merged.csv")
    merged14= pd.read_csv(merged2014Path)
    merged2015Path= Path(current_directory+r"\BDA-project\data\processed\2015merged.csv")
    merged15= pd.read_csv(merged2015Path)
    merged2016Path= Path(current_directory+r"\BDA-project\data\processed\2016merged.csv")
    merged16= pd.read_csv(merged2016Path)
    merged2017Path= Path(current_directory+r"\BDA-project\data\processed\2017merged.csv")
    merged17= pd.read_csv(merged2017Path)
    merged2018Path= Path(current_directory+r"\BDA-project\data\processed\2018merged.csv")
    merged18= pd.read_csv(merged2018Path)
    merged2019Path= Path(current_directory+r"\BDA-project\data\processed\2019merged.csv")
    merged19= pd.read_csv(merged2019Path)
    merged2020Path= Path(current_directory+r"\BDA-project\data\processed\2020merged.csv")
    merged20= pd.read_csv(merged2020Path)

    pre18FWI4Count = pre18risk.FWI_index.count()
    pre19FWI4Count = pre_risk.FWI_index.count()
    post18FWI4Count = post_risk.FWI_index.count()
    fwi4_00_count = risk00.FWI_index.count()
    fwi4_01_count = risk01.FWI_index.count()
    fwi4_02_count = risk02.FWI_index.count()
    fwi4_03_count = risk03.FWI_index.count()
    fwi4_04_count = risk04.FWI_index.count()
    fwi4_05_count = risk05.FWI_index.count()
    fwi4_06_count = risk06.FWI_index.count()
    fwi4_07_count = risk07.FWI_index.count()
    fwi4_08_count = risk08.FWI_index.count()
    fwi4_09_count = risk09.FWI_index.count()
    fwi4_10_count = risk10.FWI_index.count()
    fwi4_11_count = risk11.FWI_index.count()
    fwi4_12_count = risk12.FWI_index.count()
    fwi4_13_count = risk13.FWI_index.count()
    fwi4_14_count = risk14.FWI_index.count()
    fwi4_15_count = risk15.FWI_index.count()
    fwi4_16_count = risk16.FWI_index.count()
    fwi4_17_count = risk17.FWI_index.count()
    fwi4_18_count = risk18.FWI_index.count()
    fwi4_19_count = risk19.FWI_index.count()
    fwi4_20_count = risk20.FWI_index.count()
    pre18FWI4Fires = pre18merged.FWI_index.count()
    pre19FWI4Fires = pre_merged.FWI_index.count()
    post18FWI4Fires = post_merged.FWI_index.count()
    fwi4_00_fires_count = merged00.FWI_index.count()
    fwi4_01_fires_count = merged01.FWI_index.count()
    fwi4_02_fires_count = merged02.FWI_index.count()
    fwi4_03_fires_count = merged03.FWI_index.count()
    fwi4_04_fires_count = merged04.FWI_index.count()
    fwi4_05_fires_count = merged05.FWI_index.count()
    fwi4_06_fires_count = merged06.FWI_index.count()
    fwi4_07_fires_count = merged07.FWI_index.count()
    fwi4_08_fires_count = merged08.FWI_index.count()
    fwi4_09_fires_count = merged09.FWI_index.count()
    fwi4_10_fires_count = merged10.FWI_index.count()
    fwi4_11_fires_count = merged11.FWI_index.count()
    fwi4_12_fires_count = merged12.FWI_index.count()
    fwi4_13_fires_count = merged13.FWI_index.count()
    fwi4_14_fires_count = merged14.FWI_index.count()
    fwi4_15_fires_count = merged15.FWI_index.count()
    fwi4_16_fires_count = merged16.FWI_index.count()
    fwi4_17_fires_count = merged17.FWI_index.count()
    fwi4_18_fires_count = merged18.FWI_index.count()
    fwi4_19_fires_count = merged19.FWI_index.count()
    fwi4_20_fires_count = merged20.FWI_index.count()

    fires_per_FWI4_pre_18 = pre18FWI4Fires/pre18FWI4Count
    fires_per_FWI4_pre = pre19FWI4Fires/pre19FWI4Count
    fires_per_FWI4_post = post18FWI4Fires/post18FWI4Count
    fires_per_FWI4_00 = fwi4_00_fires_count/fwi4_00_count
    fires_per_FWI4_01 = fwi4_01_fires_count/fwi4_01_count
    fires_per_FWI4_02 = fwi4_02_fires_count/fwi4_02_count
    fires_per_FWI4_03 = fwi4_03_fires_count/fwi4_03_count
    fires_per_FWI4_04 = fwi4_04_fires_count/fwi4_04_count
    fires_per_FWI4_05 = fwi4_05_fires_count/fwi4_05_count
    fires_per_FWI4_06 = fwi4_06_fires_count/fwi4_06_count
    fires_per_FWI4_07 = fwi4_07_fires_count/fwi4_07_count
    fires_per_FWI4_08 = fwi4_08_fires_count/fwi4_08_count
    fires_per_FWI4_09 = fwi4_09_fires_count/fwi4_09_count
    fires_per_FWI4_10 = fwi4_10_fires_count/fwi4_10_count
    fires_per_FWI4_11 = fwi4_11_fires_count/fwi4_11_count
    fires_per_FWI4_12 = fwi4_12_fires_count/fwi4_12_count
    fires_per_FWI4_13 = fwi4_13_fires_count/fwi4_13_count
    fires_per_FWI4_14 = fwi4_14_fires_count/fwi4_14_count
    fires_per_FWI4_15 = fwi4_15_fires_count/fwi4_15_count
    fires_per_FWI4_16 = fwi4_16_fires_count/fwi4_16_count
    fires_per_FWI4_17 = fwi4_17_fires_count/fwi4_17_count
    fires_per_FWI4_18 = fwi4_18_fires_count/fwi4_18_count
    fires_per_FWI4_19 = fwi4_19_fires_count/fwi4_19_count
    fires_per_FWI4_20 = fwi4_20_fires_count/fwi4_20_count

    data = {'Period': ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2000-2017', '2000-2018', '2019-2020'], 
    'FWI_index => 4' : [fwi4_00_count, fwi4_01_count, fwi4_02_count, fwi4_03_count, fwi4_04_count, fwi4_05_count, fwi4_06_count, fwi4_07_count, fwi4_08_count, fwi4_09_count, fwi4_10_count, fwi4_11_count, fwi4_12_count, fwi4_13_count, fwi4_14_count, fwi4_15_count, fwi4_16_count, fwi4_17_count, fwi4_18_count, fwi4_19_count, fwi4_20_count, pre18FWI4Count, pre19FWI4Count, post18FWI4Count],
     'Fires during FWI_index => 4': [fwi4_00_fires_count, fwi4_01_fires_count, fwi4_02_fires_count, fwi4_03_fires_count, fwi4_04_fires_count, fwi4_05_fires_count, fwi4_06_fires_count, fwi4_07_fires_count, fwi4_08_fires_count, fwi4_09_fires_count, fwi4_10_fires_count, fwi4_11_fires_count, fwi4_12_fires_count, fwi4_13_fires_count, fwi4_14_fires_count, fwi4_15_fires_count, fwi4_16_fires_count, fwi4_17_fires_count, fwi4_18_fires_count, fwi4_19_fires_count, fwi4_20_fires_count, pre18FWI4Fires, pre19FWI4Fires, post18FWI4Fires],
      'Fires per FWI_index => 4' : [fires_per_FWI4_00, fires_per_FWI4_01, fires_per_FWI4_02, fires_per_FWI4_03, fires_per_FWI4_04, fires_per_FWI4_05, fires_per_FWI4_06, fires_per_FWI4_07, fires_per_FWI4_08, fires_per_FWI4_09, fires_per_FWI4_10, fires_per_FWI4_11, fires_per_FWI4_12, fires_per_FWI4_13, fires_per_FWI4_14, fires_per_FWI4_15, fires_per_FWI4_16, fires_per_FWI4_17, fires_per_FWI4_18, fires_per_FWI4_19, fires_per_FWI4_20, fires_per_FWI4_pre_18, fires_per_FWI4_pre, fires_per_FWI4_post]}
    
    firesPerFWIdf = pd.DataFrame(data)
   
    ax = plt.subplot(111, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, firesPerFWIdf, loc='center')
    # draw canvas once
    plt.gcf().canvas.draw()
    # get bounding box of table
    points = ax.get_window_extent(plt.gcf()._cachedRenderer).get_points()
    # add 10 pixel spacing
    points[0,:] -= 10; points[1,:] += 10
    # get new bounding box in inches
    nbbox = matplotlib.transforms.Bbox.from_extents(points/plt.gcf().dpi)
  
    path = Path(current_directory+r"\BDA-project\reports\figures\fwi4table")
    
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