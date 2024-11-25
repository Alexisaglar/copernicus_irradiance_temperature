
# Copernicus Irradiance and Temperature Data Analysis

This repository is dedicated to the analysis and exploration of solar irradiance and temperature data using resources from the Copernicus Climate Data Store (CDS). The repository includes Python scripts and Jupyter notebooks for data retrieval, processing, visualization, and analysis.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Data Source](#data-source)
- [Contributing](#contributing)

---

## Overview

The **Copernicus Irradiance and Temperature** project is designed to analyze solar irradiance and temperature data for various geographical locations. This repository focuses on:

- Retrieving data from the Copernicus Climate Data Store (CDS).
- Visualizing patterns and trends in solar irradiance and temperature.
- Performing statistical and spatial analyses to better understand climatic variations.

---

## Features

- **Data Retrieval**: Fetch irradiance and temperature data directly from CDS using Python APIs.
- **Data Cleaning and Processing**: Includes scripts to preprocess and clean raw data for analysis.
- **Visualization Tools**: Generate insightful visualizations to explore temporal and spatial patterns.
- **Customizable Analyses**: Scripts can be easily adapted to analyze specific regions or timeframes.

---

## Requirements

Before running the scripts, ensure you have the following installed:

- Python 3.7+
- Required Python packages (see `requirements.txt`):
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `xarray`
  - `netCDF4`
  - `cdsapi`
  - Other dependencies as listed in the `requirements.txt`

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Alexisaglar/copernicus_irradiance_temperature.git
   cd copernicus_irradiance_temperature
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Data Retrieval
Use the provided scripts to download solar irradiance and temperature data from CDS. Make sure to configure your CDS API key in the `~/.cdsapirc` file.

### 2. Data Processing
Run the preprocessing scripts to clean and structure the data for analysis.

### 3. Analysis and Visualization
Use Python scripts to perform exploratory data analysis (EDA) and generate visualizations.

---

## Data Source

The data used in this repository is sourced from the [Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu/). Ensure you have an active account with CDS and have configured the API key before running the scripts.

---

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to report issues, please open an issue or submit a pull request.

---
## Acknowledgements

- [Copernicus Climate Change Service (C3S)](https://climate.copernicus.eu/)

--- 
