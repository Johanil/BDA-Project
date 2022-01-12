BDA-Project
==============================

This is a big data analytics project to examine if the ban of sales of disposable BBQ-grills when the FWI-index is four or above have had any impact on the forest fires in Sweden. 

Make commands
------------

data: Run this make command which preproccess the data and creates all nessecary datasets used for analysis in this project.
visualize: Run this make command to create plots and tables.

More information about makefiles can be found here: https://www.gnu.org/software/make/manual/make.html (2022-01-12)

Data
------------
Because of the files sizes, the fire risk data set and the reported fires dataset only have sample samples included. To retrieve complete dataset go to Data Access

Fire risk data
------------
The fire risk dataset contains 23 columns, below you'll find an explaination for each of the X columns used in this project.
| Column names    | Explaination                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PunktID    | ID for measuring stations                                                                                                                                                                                                                                                                                                                                                                                      |
| Kommun     | Municipality code                                                                                                                                                                                                                                                                                                                                                                                              |
| Datum      | Date                                                                                                                                                                                                                                                                                                                                                                                                           |
| FWI        | Fire Weather Index, the number representing the risk of fire also meant to mirror the fire in                                                                                                                                                                                                                                                                                                                  |
| FWI\_index | In Sweden FWI has been translated to a firerisk index with six classifications with increasing risk of fire for each increment in the index. This is used for communication to the public and media. The classifications are. 1: Very small fire risk <5, 2: Small fire risk 6-11, 3: Moderate risk of fire 12-16, 4: Great risk of fire 17-21, 5: Very great risk of fire 22-27, 5E: Extreme risk of fire >28 |


Column information is retrieved from:
https://www.msb.se/contentassets/319560083841487f84dbbad048c84152/brand-fakta.pdf (2022-01-11)

The following is an example of a row from the fire risk dataset, note that  PunktID, Kommun, Datum, FWI and FWI-index are the only values used for this projects analysis.

| PunktID | E      | N       | Kommun | Datum      | Temp | Tmedel | Nederbord | RH   | Vindhastighet | Vindriktning | FFMC | DMC | DC    | ISI | BUI | FWI | FWI\_index | HBV\_o | HBV\_u | HBV | HBV\_index | Gras | 
| ------- | ------ | ------- | ------ | ---------- | ---- | ------ | --------- | ---- | ------------- | ------------ | ---- | --- | ----- | --- | --- | --- | ---------- | ------ | ------ | --- | ---------- | ---- |
| 14      | 474160 | 6467091 | 509    | 2019-05-23 | 12,2 | 11     | 6,3       | 69,6 | 5             | 204,6        | 45,5 | 2,7 | 145,6 | 0,2 | 5,2 | 0,1 | 1          | 85     | 45     | 87  | 1          | 2    |  

Reported fires data
------------
| Column names      | Explaination         |
| ----------------- | -------------------- |
| ar                | Year                 |
| datum             | Date                 |              
| kommun            | Municipality code    |
| kommunKortnamn    | Name of municipality |
| BEJbrandorsakText | Cause of fire        |

| ar   | datum     | tid   | kommun | kommunKortNamn | verksamhetText                         | sweref99Norr | sweref99Ost | BEJBbrandorsakText       | areaIProduktivSkogsmark\_m2 | areaIAnnanTradbevuxenMark\_m2 | areaIMarkUtanTrad\_m2 |
| ---- | --------- | ----- | ------ | -------------- | -------------------------------------- | ------------ | ----------- | ------------------------ | --------------------------- | ----------------------------- | --------------------- |
| 2010 | 2010-04-14 | 18:18 | 1382   | Falkenberg     | Verksamhet inte knuten till en byggnad | 6306404      | 348526      | Grillning eller lägereld | 0  | 0                             | 4000                  |



Municipality data
---
The topojson data used in this project was retrieved from the following github repository: https://github.com/deldersveld/topojson/blob/master/countries/sweden/sweden-municipalities.json (2022-01-12)
Municipalities in Sweden all have a municipality code, information about what code a certain municipality have can be found here: https://skr.se/skr/tjanster/kommunerochregioner/faktakommunerochregioner/kommunkoder.2052.html
More information about the topojson datatype can be found here: https://github.com/topojson/topojson (2022-01-12)

Data Access
---
By contacting the swedish contingency agency (MSB) at the following email: Statistik@MSB.se you can retreive the complete dataset with reported fires. Make sure to request a complete dataset with information about reported fire indicents between 2000-2020 (or later). For access to fire risk data use the same email adress and request information about FWI measurements between the same years.
Some information can be access through the IDA data portal which is reached at the following adress: https://ida.msb.se/ (2022-01-12)

Other
------------

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make visulization`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
