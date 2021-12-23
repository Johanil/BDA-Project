# -*- coding: utf-8 -*-
import click
import os
import logging
import pandas as pd
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from preprocessing import PreProcessMerge, PreProcessReported, PreProcessRisk, PreProcessFigures
import os
current_directory = os.getcwd()
#@click.command()
#@click.argument('input_filepath', type=click.Path(exists=True))
#@click.argument('output_filepath', type=click.Path())
def main():
    #Paths for raw datasets
    risk_path = Path(current_directory+r"\BDA-project\data\raw\Brandriskdata 2000-2020.csv")
    fire_path = Path(current_directory+r"\BDA-project\data\raw\Insatser till brand i skog och mark 2000-2020.xlsx")
    #Raw data read
    types={ 'PunktID': str}
    df_risk_data = pd.read_csv(risk_path,sep=';', dtype=types,)
    df_fire_data = pd.read_excel(fire_path)
    #Preprocess class instansiation
    ppr = PreProcessRisk()
    ppf = PreProcessReported()
    ppm = PreProcessMerge()
    ppfig = PreProcessFigures()
    #Preprocessing datasets
    processed_risk_data= ppr.process_dataframe(dataset=df_risk_data)
    processed_fire_data = ppf.process_dataframe(df_fire_data)
    #Merge preprocessed datasets
    processed_merged = ppm.process_dataframe(processed_risk_data, processed_fire_data)
    processed_merged_fwi4 = ppm.process_dataframe(processed_risk_data, processed_fire_data, 4)
    #Save merged preprocessed dataset to csv
    processed_merged.to_csv(r'C:\BDA-Project\BDA-project\data\processed\FiresWithRisks 2000-2020.csv')

    #?????
    pre_risk, post_risk, risk2018, risk2019, risk2020 = ppr.process_dataframe_fwi4_days(ppr.process_dataframe(df_risk_data))
    pre_merged, post_merged, merged_2018, merged_2019, merged_2020 = ppm.process_dataframe_fwi4_days(processed_merged_fwi4)

    #Time grouped csv files pre disopsable barbeque "ban"
    pre_risk.to_csv(current_directory+r"\BDA-project\data\processed\pre19fwi4Risk.csv")
    post_risk.to_csv(current_directory+r"\BDA-project\data\processed\post18fwi4Risk.csv")
    pre_merged.to_csv(current_directory+r"\BDA-project\data\processed\pre19fwi4Merged.csv")
    post_merged.to_csv(current_directory+r"\BDA-project\data\processed\post18fwi4Merged.csv")
    merged_2018.to_csv(current_directory+r"\BDA-project\data\processed\2018merged.csv")
    merged_2019.to_csv(current_directory+r"\BDA-project\data\processed\2019merged.csv")
    merged_2020.to_csv(current_directory+r"\BDA-project\data\processed\2020merged.csv")
    risk2018.to_csv(current_directory+r"\BDA-project\data\processed\risk2018.csv")
    risk2019.to_csv(current_directory+r"\BDA-project\data\processed\risk2019.csv")
    risk2020.to_csv(current_directory+r"\BDA-project\data\processed\risk2020.csv")


    #YOU ARE HERE
    #Creating df for plots to save as csv
    plot4fwi = ppm.process_dataframe(processed_risk_data, processed_fire_data, 4)
    plot0fwi = ppm.process_dataframe(processed_risk_data, processed_fire_data)
    #Creating df for choropleth map df to save as csv
    map4fwi = ppfig.make_clo_map_csv(ppm.process_dataframe(processed_risk_data, processed_fire_data, 4))
    map0fwi = ppfig.make_clo_map_csv(ppm.process_dataframe(processed_risk_data, processed_fire_data))
    fire_muni_pre2019 = ppfig.make_clo_map_csv()
    fire_muni_post2018 = ppfig.make_clo_map_csv()
    #Save choroleth mp as csv
    map4fwi.to_csv(current_directory+r"\BDA-project\data\processed\choropleth\firesfwi4_choropleth.csv")
    map0fwi.to_csv(current_directory+r"\BDA-project\data\processed\choropleth\firesfwi0_choropleth.csv")

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

