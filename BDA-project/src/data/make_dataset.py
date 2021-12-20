# -*- coding: utf-8 -*-
import click
import os
import logging
import pandas as pd
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from preprocessing import PreProcessMerge, PreProcessReported, PreProcessRisk

#@click.command()
#@click.argument('input_filepath', type=click.Path(exists=True))
#@click.argument('output_filepath', type=click.Path())
def main():
    risk_path = Path(r"C:\BDA-Project\BDA-project\data\raw\Brandriskdata 2000-2020.csv")
    fire_path = Path(r"C:\BDA-Project\BDA-project\data\raw\Insatser till brand i skog och mark 2000-2020.xlsx")
    types={ 'PunktID': str}
    df_risk_data = pd.read_csv(risk_path,sep=';', dtype=types,)
    df_fire_data = pd.read_excel(fire_path)
    ppr = PreProcessRisk()
    ppf = PreProcessReported()
    ppm = PreProcessMerge()
    processed_risk_data= ppr.process_dataframe(dataset=df_risk_data)
    processed_fire_data = ppf.process_dataframe(df_fire_data)
    processed_merged = ppm.process_dataframe(processed_risk_data, processed_fire_data)
    print(processed_merged)
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    #output_path = Path(r"F:\Code\BDA-Project\BDA-project\data\processed")
    #file = Path(r"\FiresWithRisks.csv")
    processed_merged.to_csv('C:\BDA-Project\BDA-project\data\processed\FiresWithRisks 2000-2020.csv')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

