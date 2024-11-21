# `ACTIVATE_CCN_closure`

This repository contains the scripts used to perform CCN closure on the NASA ACTIVATE dataset.

## Setting up virtual environment

To reproduce the results, create a virtual environment with Python and install the requirements from the `requirements.txt` document to ensure the code runs successfully.

This project uses Python 3.13.0 which is available for download at [https://www.python.org/downloads/](https://www.python.org/downloads/).

To create a virtual environment called `ccn_closure` using the `requirements.txt` file for a UNIX system, navigate to the directory of the project and run the following commands consecutively.

```
python -m venv ccn_closure
source ccn_closure/bin/activate
python -m pip install -r requirements.txt
```

## Files

---
### `./data`

This is the directory to put the data from the ACTIVATE mission. The data can be downloaded from the NASA LaRC Suborbital Science Data for Atmospheric Composition website: [https://www-air.larc.nasa.gov/missions/activate/index.html](https://www-air.larc.nasa.gov/missions/activate/index.html).

---
### `./figures`

Directory for saving figures exported from the scripts.

---
### `./scripts`

Contains the scripts which I run to perform closure analysis. Numbers provided at beginning of file name to specify the order which files should be run. When the numbers are the same, it means the scripts can be run concurrently as long as the preceding scripts were run.

#### `01_file_merger.ipynb`

This script merges the data into a single table and saves it as a CSV in the `/tables` folder.

#### `02_find_obs_kappa.ipynb`

This script uses `closure_funcs.py` to find the activation diameter observed from the data and the corresponding kappa value implied for the given CCN instrument supersaturation.

#### `03_AMS_fit_only_OMF.ipynb`

Attempts to fit observed kappa with calculated kappa from AMS. Treats non-organics as one species.

#### `03_AMS_fit.ipynb`

Attempts to fit observed kappa with calculated kappa from AMS.

#### `03_closure_calc_CO.ipynb`

Calculates predicted CCN concentration using CO as a proxy for aerosol chemistry.

#### `03_closure_calc_E3SM_non_org.ipynb`

This script calculates the predicted CCN concentration given the kappa values of the E3SM model and the volume fractions from the AMS. Treats non-organics as one species.

#### `03_closure_calc_E3SM.ipynb`

This script calculates the predicted CCN concentration given the kappa values of the E3SM model and the volume fractions from the AMS.

#### `03_closure_calc_fit_k.ipynb`

This script calculates the predicted CCN concentration given the kappa values of the observed kappa fit and the volume fractions from the AMS. Treats non-organics as one species.

#### `03_closure_calc_single_k.ipynb`

This script calculates the predicted CCN concentration given a single kappa values and the volume fractions from the AMS. Treats non-organics as one species.

#### `04_map_plot.ipynb`

Plot results on map.

#### `04_plots.ipynb`

Plot results.

#### `closure_funcs.py`

This script contains the functions used to calculate activation diameter and kappa. These functions are imported into the relevant Jupyter notebooks.

---
#### `./scripts/dev_scripts`

This folder contains scripts more in the development stage.

##### `archived_plots.ipynb`

This script contains plots which are in development.

##### `compare_closure_calc_E3SM.ipynb`

This script was used to diagnose an issue I was having with particle integration.

##### `compare_find_obs_kappa.ipynb`

Diagnostic script.

##### `compare_func.ipynb`

Used to compare a different method for solving Köhler theory.

##### `compare.ipynb`

Used to assess the performance of leg mean closure.

##### `ml_k_test.ipynb`

A test to see if k_obs can be predicted with machine learning with AMS values as input.

---
### `./tables`

Directory for CSV tables exported from scripts.

---
### `requirements.txt`

This file contains the Python environment which I used to run my scripts.

---