# Mining Prospectivity Chile

![mining](images/heavy-machinery-used-construction-industry-engineering.jpg)

## Introduction
Mining exploration can be expensive, especially when large areas need to be evaluated. Prioritizing areas with higher prospectivity can help focus exploration efforts on locations that are more likely to contain mineral deposits. However, mining exploration involves a large number of measurements and geographic factors, which can make them difficult to visualize and analyze using simple charts. 

## Overview
In this project, Machine Learning is used to identify patterns in sediment geochemistry measurements and distinguish between areas with higher and lower prospectivity. This project considers large-scale mining prospectivity across Chile, using measurements collected from different locations.

The focus is on building a practical end-to-end application, from data collection and preprocessing to model training and visualization.

## Data Sources
The datasets used in this project are provided by SERNAGEOMIN (Servicio Nacional de Geología y Minería de Chile).

The data was accessed in September 2026 and includes information related to mining facilities, geochemistry, and other geographic and geological factors used in the analysis.

## Repository

### File System
The current repository keeps the following structure.
```
prospectivity/
├── data/
│   ├── raw/ # Raw datasets from SERNAGEOMIN
│   ├── interim/ # Intermediate preprocessed datasets
│   └── processed/ # Datasets ready for Machine Learning
├── images/ # Saved Matplotlib figures
├── models/ # Saved trained models
├── notebooks/
│   └── Iteration 1/
│       ├── data_collection.ipynb # Data collection process
│       └── data_processing_modeling.ipynb # Data processing and machine learning
├── src/
│   └── prospectivity/
│       ├── __init__.py
│       ├── main.py # FastAPI server for the prospectivity map and inference
│       ├── preprocessing.py # Preprocessing methods used for prediction
│       └── schemas.py # Pydantic schemas
├── .env.example # Environment variables, such as the Mapbox API key
├── Dockerfile # Docker configuration for deployment
├── pyproject.toml
└── uv.lock
```

### Installation
There are two types of dependencies: general and development dependencies.

You can use the standard `uv sync` command to install all dependencies. If you only want to run the FastAPI server, you can use  `uv sync --no-dev` to skip the dependencies used by the notebooks.

This project uses uv ` 0.12.9` and Python `3.11.16`.

If you want to use the notebooks, please refer to `.env.example` to create your own `.env` and add your Mapbox API key to view the maps.

### Machine Learning

There are two notebooks in the `/notebooks/Iteration 1` directory where you can see the detailed process, from collecting data from SERNAGEOMIN servers and preprocessing the data to training and comparing different models, and finally evaluating and selecting a model.

### Links
You can use the web app to visualize the prospectivity map, explore measurement details, and predict the prospectivity of a new measurement.

Web App: https://prospectivity.olver.site/map

You can also use the API directly or view its documentation.

API Docs: https://api.prospectivity.olver.site/docs

You can also view the web application repository on GitHub: https://github.com/OlverArceL01/Prospectivity-app