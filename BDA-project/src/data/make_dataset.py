# -*- coding: utf-8 -*-
import click
import os
import logging
import pandas as pd
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from preprocessing import PreProcessMerge, PreProcessReported, PreProcessRisk, PreProcessTables
import os
current_directory = os.getcwd()

def main():
    risk_path = Path(current_directory+r"\BDA-project\data\raw\Brandriskdata 2000-2020.csv")
    fire_path = Path(current_directory+r"\BDA-project\data\raw\Insatser till brand i skog och mark 2000-2020.xlsx")
    types={ 'PunktID': str}
    print("Reading csv files...")
    df_risk_data = pd.read_csv(risk_path,sep=';', dtype=types,)
    print("Firerisk data ingested")
    df_fire_data = pd.read_excel(fire_path)
    print("Reported fires ingested")
    ppr = PreProcessRisk()
    ppf = PreProcessReported()
    ppm = PreProcessMerge()
    ppt = PreProcessTables()
    processed_risk_data= ppr.process_dataframe(dataset=df_risk_data)
    processed_fire_data = ppf.process_dataframe(df_fire_data)
    processed_merged = ppm.process_dataframe(processed_risk_data, processed_fire_data)
    logger = logging.getLogger(__name__)
    logger.info('Making final datasets from raw data')

    month_year = ppt.month_year(processed_merged)
    month_year.to_csv(current_directory+r"\BDA-project\data\processed\month_year.csv")
    fires_day_month = ppt.fires_day_month(month_year)
    fires_day_month_rol14_mean = ppt.fires_day_month_rol14_mean(fires_day_month)
    fires_day_month_rol14_mean.to_csv(current_directory+r"\BDA-project\data\processed\fires_day_month_rol14_mean.csv")

    fire_muni_pre2019, fire_muni_post2018, allyears = ppt.fire_muni(processed_merged)

    fire_muni_pre2019.to_csv(current_directory+r"\BDA-project\data\processed\fire_muni_pre2019.csv")
    fire_muni_post2018.to_csv(current_directory+r"\BDA-project\data\processed\fire_muni_post2018.csv")
    allyears.to_csv(current_directory+r"\BDA-project\data\processed\allyears.csv")

    processed_merged.to_csv(current_directory+r"\BDA-project\data\processed\FiresWithRisks 2000-2020.csv")

    pre18risk, pre_risk, post_risk, risk2000, risk2001, risk2002, risk2003, risk2004, risk2005, risk2006, risk2007, risk2008, risk2009, risk2010, risk2011, risk2012, risk2013, risk2014, risk2015, risk2016, risk2017, risk2018, risk2019, risk2020 = ppr.process_dataframe_fwi4_days(ppr.process_dataframe(df_risk_data))
 
    processed_merged_fwi4 = ppm.process_dataframe(processed_risk_data, processed_fire_data, 4)
    pre18merged, pre_merged, post_merged, merged_2000, merged_2001, merged_2002, merged_2003, merged_2004, merged_2005, merged_2006, merged_2007, merged_2008, merged_2009, merged_2010, merged_2011, merged_2012, merged_2013, merged_2014, merged_2015, merged_2016, merged_2017, merged_2018, merged_2019, merged_2020 = ppm.process_dataframe_fwi4_days(processed_merged_fwi4)
    print("Writing csv files to \processed\.. directory..")

    pre18risk.to_csv(current_directory+r"\BDA-project\data\processed\pre18fwi4Risk.csv")
    pre_risk.to_csv(current_directory+r"\BDA-project\data\processed\pre19fwi4Risk.csv")
    post_risk.to_csv(current_directory+r"\BDA-project\data\processed\post18fwi4Risk.csv")
    risk2000.to_csv(current_directory+r"\BDA-project\data\processed\risk2000.csv")
    risk2001.to_csv(current_directory+r"\BDA-project\data\processed\risk2001.csv")
    risk2002.to_csv(current_directory+r"\BDA-project\data\processed\risk2002.csv")
    risk2003.to_csv(current_directory+r"\BDA-project\data\processed\risk2003.csv")
    risk2004.to_csv(current_directory+r"\BDA-project\data\processed\risk2004.csv")
    risk2005.to_csv(current_directory+r"\BDA-project\data\processed\risk2005.csv")
    risk2006.to_csv(current_directory+r"\BDA-project\data\processed\risk2006.csv")
    risk2007.to_csv(current_directory+r"\BDA-project\data\processed\risk2007.csv")
    risk2008.to_csv(current_directory+r"\BDA-project\data\processed\risk2008.csv")
    risk2009.to_csv(current_directory+r"\BDA-project\data\processed\risk2009.csv")
    risk2010.to_csv(current_directory+r"\BDA-project\data\processed\risk2010.csv")
    risk2011.to_csv(current_directory+r"\BDA-project\data\processed\risk2011.csv")
    risk2012.to_csv(current_directory+r"\BDA-project\data\processed\risk2012.csv")
    risk2013.to_csv(current_directory+r"\BDA-project\data\processed\risk2013.csv")
    risk2014.to_csv(current_directory+r"\BDA-project\data\processed\risk2014.csv")
    risk2015.to_csv(current_directory+r"\BDA-project\data\processed\risk2015.csv")
    risk2016.to_csv(current_directory+r"\BDA-project\data\processed\risk2016.csv")
    risk2017.to_csv(current_directory+r"\BDA-project\data\processed\risk2017.csv")
    risk2018.to_csv(current_directory+r"\BDA-project\data\processed\risk2018.csv")
    risk2019.to_csv(current_directory+r"\BDA-project\data\processed\risk2019.csv")
    risk2020.to_csv(current_directory+r"\BDA-project\data\processed\risk2020.csv")
    pre18merged.to_csv(current_directory+r"\BDA-project\data\processed\pre18fwi4Merged.csv")
    pre_merged.to_csv(current_directory+r"\BDA-project\data\processed\pre19fwi4Merged.csv")
    post_merged.to_csv(current_directory+r"\BDA-project\data\processed\post18fwi4Merged.csv")
    merged_2000.to_csv(current_directory+r"\BDA-project\data\processed\2000merged.csv")
    merged_2001.to_csv(current_directory+r"\BDA-project\data\processed\2001merged.csv")
    merged_2002.to_csv(current_directory+r"\BDA-project\data\processed\2002merged.csv")
    merged_2003.to_csv(current_directory+r"\BDA-project\data\processed\2003merged.csv")
    merged_2004.to_csv(current_directory+r"\BDA-project\data\processed\2004merged.csv")
    merged_2005.to_csv(current_directory+r"\BDA-project\data\processed\2005merged.csv")
    merged_2006.to_csv(current_directory+r"\BDA-project\data\processed\2006merged.csv")
    merged_2007.to_csv(current_directory+r"\BDA-project\data\processed\2007merged.csv")
    merged_2008.to_csv(current_directory+r"\BDA-project\data\processed\2008merged.csv")
    merged_2009.to_csv(current_directory+r"\BDA-project\data\processed\2009merged.csv")
    merged_2010.to_csv(current_directory+r"\BDA-project\data\processed\2010merged.csv")
    merged_2011.to_csv(current_directory+r"\BDA-project\data\processed\2011merged.csv")
    merged_2012.to_csv(current_directory+r"\BDA-project\data\processed\2012merged.csv")
    merged_2013.to_csv(current_directory+r"\BDA-project\data\processed\2013merged.csv")
    merged_2014.to_csv(current_directory+r"\BDA-project\data\processed\2014merged.csv")
    merged_2015.to_csv(current_directory+r"\BDA-project\data\processed\2015merged.csv")
    merged_2016.to_csv(current_directory+r"\BDA-project\data\processed\2016merged.csv")
    merged_2017.to_csv(current_directory+r"\BDA-project\data\processed\2017merged.csv")
    merged_2018.to_csv(current_directory+r"\BDA-project\data\processed\2018merged.csv")
    merged_2019.to_csv(current_directory+r"\BDA-project\data\processed\2019merged.csv")
    merged_2020.to_csv(current_directory+r"\BDA-project\data\processed\2020merged.csv")

    print("All files processed!")
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

