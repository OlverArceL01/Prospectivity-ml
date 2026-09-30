import json
import joblib
import numpy as np
import pandas as pd
import geopandas as gpd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .measurement_schema import Measurement
from fastapi.middleware.cors import CORSMiddleware
from .preprocessing import formatting_numeric_values, add_categorical_columns, fill_with_median, logarithm_transformation

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://prospectivity.olver.site",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = joblib.load("models/logistic_regression.joblib")

@app.get("/")
def root():
    return {"message": "Prospectivity API"}
@app.get("/prospectivity-map")
def prospectivity_map():
    gdf = gpd.read_parquet("data/processed/prospectivity_map.parquet")
    gdf = gdf[["OBJECTID_left", "SHAPE", "probability"]]
    gdf = gdf.to_crs(4326)
    geojson = gdf.to_json()
    return JSONResponse(content=json.loads(geojson))

@app.get("/prospectivity-map-measurement/{id}")
def prospectivity_map_measurement(id: int):
    gdf = gpd.read_parquet("data/processed/prospectivity_map.parquet")
    measurement = gdf[gdf["OBJECTID_left"] == id]
    if measurement.empty:
        raise HTTPException(status_code=404, detail="Measurement not found")
    measurement = measurement.to_crs(4326)
    feature = json.loads(measurement.to_json())["features"][0]
    return feature

@app.post("/predict-sample-prospectivity")
def predict_sample_prospectivity(measurement: Measurement):
    df = pd.DataFrame([measurement.model_dump()])
    df = formatting_numeric_values(df)
    df = add_categorical_columns(df)
    measurements_df = gpd.read_parquet("data/interim/measurements_without_log_df.parquet")
    measurements_df = formatting_numeric_values(measurements_df)
    df = fill_with_median(df, measurements_df)
    df = logarithm_transformation(df)
    cols = [
        'CTOTAL___', 'STOTAL__', 'Suma', 'LOI', 'SiO2', 'Al2O3', 'Fe2O3', 'MgO', 'CaO', 'Na2O', 'K2O', 'TiO2', 'P2O5', 'MnO', 'Cr2O3',
        'Sc', 'Ba', 'Be', 'Co', 'Cs', 'Ga', 'Hf', 'Nb', 'Rb', 'Sn', 'Sr', 'Ta', 'Th', 'U', 'V', 'W', 'Zr', 'Y', 'La', 'Ce', 'Pr', 'Nd',
        'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Mo', 'Cu', 'Pb', 'Zn', 'Ni', 'As_', 'Cd', 'Sb', 'Bi', 'Ag', 'Au',
        'Hg', 'Tl', 'Se', 'Te_ppm', 'B_ppm', 
        
        'CTOTAL____isna', 'STOTAL___isna', 'SiO2_isna', 'Al2O3_isna', 'Fe2O3_isna', 'MgO_isna',
        'CaO_isna', 'Na2O_isna', 'K2O_isna', 'TiO2_isna', 'P2O5_isna', 'MnO_isna', 'Cr2O3_insufficient_sample', 'Cr2O3_<0.002',
        'LOI_isna', 'Suma_isna', 'Sc_isna', 'Ba_isna', 'Be_insufficient_sample', 'Be_<1.0', 'Co_isna', 'Cs_isna', 'Ga_isna', 'Hf_isna',
        'Nb_isna', 'Rb_isna', 'Sn_insufficient_sample', 'Sn_<1.0', 'Sr_isna', 'Ta_isna', 'Th_isna', 'U_isna', 'V_isna', 'W_isna',
        'Zr_isna', 'Y_isna', 'La_isna', 'Ce_isna', 'Pr_isna', 'Nd_isna', 'Sm_isna', 'Eu_isna', 'Gd_isna', 'Tb_isna', 'Dy_isna',
        'Ho_isna', 'Er_isna', 'Tm_isna', 'Yb_isna', 'Lu_isna', 'Mo_isna', 'Cu_isna', 'Pb_isna', 'Zn_isna', 'Ni_isna', 'As__isna',
        'Cd_insufficient_sample', 'Cd_<0.1', 'Sb_insufficient_sample', 'Sb_<0.1', 'Sb_>2000.0', 'Bi_insufficient_sample', 'Bi_<0.1',
        'Ag_insufficient_sample', 'Ag_<0.1', 'Au_insufficient_sample', 'Au_<0.5', 'Hg_insufficient_sample', 'Hg_<0.01',
        'Tl_insufficient_sample', 'Tl_<0.1', 'Se_insufficient_sample', 'Se_<0.5', 'Te_ppm_isna', 'Te_ppm_<0.2', 'B_ppm_isna', 
        'B_ppm_<3.0', 'geochemistry_published'
    ]
    if set(df.columns) != set(cols):
        missing = set(cols) - set(df.columns)
        extra = set(df.columns) - set(cols)
        raise ValueError(
            f"Column mismatch. Missing: {sorted(missing)}; Extra: {sorted(extra)}"
        )
    
    df = df[model.feature_names_in_]
    probability = model.predict_proba(df)[0, 1]
    return {
        "probability": float(probability),
        "prediction": int(probability >= 0.5)
    }