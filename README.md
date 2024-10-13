# `ACTIVATE_CCN_closure`

This repository contains the scripts used to perform CCN closure on the NASA ACTIVATE dataset.

## Files

### `requirements.txt`

This file contains the python environment which I used to run my scripts. To reproduce the results, create a virtual environment with Python version 3.11.1 and the requirements from this document to ensure the code runs.

### `/tables`

CSV tables exported from scripts.

### `/scripts`

Contains the scripts which I run to perform closure analysis. Numbers provided at beginning of file name to specify the order which files should be run. When the numbers are the same, it means the scripts can be run concurrently as long as the preceding scripts were run.

#### `01_file_merger.ipynb`

This script merges the data into a single table and saves it as a CSV in the `/tables` folder.

#### `closure_funcs.py`

This script contains the functions used to calculate activation diameter and kappa. These functions are imported into the relevant Jupyter notebooks.