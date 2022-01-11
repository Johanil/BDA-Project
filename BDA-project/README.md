BDA-Project
==============================

Big data analytics project to examine if changes in sales of  disposable BBQ-grills have had any  impact on forest fires in Sweden

Make commands
------------

Data
------------
Fire risk data
------------
The fire risk dataset contains 23 columns, below you'll find an explaination for each of the X columns used in this project.



Column information is retrieved from:
https://www.msb.se/contentassets/319560083841487f84dbbad048c84152/brand-fakta.pdf (2022-01-11)

The following is an example of a row from the fire risk dataset, note that  PunktID, Kommun, Datum, FWI and FWI-index are the only values used for this projects analysis.

| PunktID | E      | N       | Kommun | Datum      | Temp | Tmedel | Nederbord | RH   | Vindhastighet | Vindriktning | FFMC | DMC | DC    | ISI | BUI | FWI | FWI\_index | HBV\_o | HBV\_u | HBV | HBV\_index | Gras | 
| ------- | ------ | ------- | ------ | ---------- | ---- | ------ | --------- | ---- | ------------- | ------------ | ---- | --- | ----- | --- | --- | --- | ---------- | ------ | ------ | --- | ---------- | ---- |
| 14      | 474160 | 6467091 | 509    | 2019-05-23 | 12,2 | 11     | 6,3       | 69,6 | 5             | 204,6        | 45,5 | 2,7 | 145,6 | 0,2 | 5,2 | 0,1 | 1          | 85     | 45     | 87  | 1          | 2    |  

Reported fires data
------------

Municipality data
---


Other
------------

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
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
