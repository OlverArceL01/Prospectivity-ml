import json
import joblib
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .schemas import Measurement, HealthResponse, PredictResponse
from fastapi.middleware.cors import CORSMiddleware
from .preprocessing import formatting_numeric_values, add_categorical_columns, fill_with_median, logarithm_transformation

app = FastAPI(
    title="Mining Prospectivity Chile API",
    description="Backend API for the Mining Prospectivity Chile web application.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    # "http://localhost:4200",
    "https://prospectivity.olver.site",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = joblib.load("models/logistic_regression.joblib")

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Mining Prospectivity Chile API"}

@app.get(
    "/health",
    summary="Check API health",
    description="Checks whether the API is running and the required model and data files are available.",
    tags=["Health"],
    response_model=HealthResponse
)
def health():
    check_files = [
        "data/processed/prospectivity_map.parquet",
        "models/logistic_regression.joblib",
        "data/interim/measurements_without_log_df.parquet",
    ]

    files_ok = all(Path(file).exists() for file in check_files)

    return {
        "status": "ok" if files_ok else "error",
        "files_available": files_ok,
    }

@app.get("/prospectivity-map",
            description="Get measurement coordinates and prospectivity probabilities from the map.",
            tags=["Prospectivity Map"],
            responses={
                200: {
                    "description": "Measurements from the prospectivity map.",
                    "content": {
                        "application/json": {
                            "example": {
                                "type": "FeatureCollection",
                                "features": [
                                    {
                                    "id": "0",
                                    "type": "Feature",
                                    "properties": {
                                        "OBJECTID_left": 1,
                                        "probability": 0.023437538217366192
                                    },
                                    "geometry": {
                                        "type": "Point",
                                        "coordinates": [
                                        -69.61552188403788,
                                        -18.68116191590786
                                        ]
                                    }
                                    }
                                ]
                            }
                        }
                    }
                }
            }
         )
def prospectivity_map():
    gdf = gpd.read_parquet("data/processed/prospectivity_map.parquet")
    gdf = gdf[["OBJECTID_left", "SHAPE", "probability"]]
    gdf = gdf.to_crs(4326)
    geojson = gdf.to_json()
    return JSONResponse(content=json.loads(geojson))

@app.get("/prospectivity-map-measurement/{id}",
            description="Get measurement details from the prospectivity map.",            
            tags=["Prospectivity Map"],
            responses={
                200: {
                    "description": "Geochemical measurement with prospectivity prediction.",
                    "content": {
                        "application/json": {
                            "example": {
                                "id": "98",
                                "type": "Feature",
                                "properties": {
                                    "OBJECTID_left": 99,
                                    "probability": 0.05176508700484972,
                                    "Proyecto": "Hoja Arica",
                                    "Punto_de_muestreo": "CR-117",
                                    "Altitud____m_s_n_m__": 3329,
                                    "UTM_ESTE__Sirgas_UTM_19S_": 428520,
                                    "UTM_NORTE__Sirgas_UTM_19S_": 7976467,
                                    "Fecha_del_muestreo": "junio 2012",
                                    "Muestra": "GQ-12-CR-025",
                                    "Duplicado_de_terreno": "Sin duplicado",
                                    "Tipo_de_muestra": "Compósito de sedimento de drenaje",
                                    "Escorrentía_en_el_momento_del_muestreo": "Sin Información",
                                    "Color": "Pardo",
                                    "Estimación_de_granulometria_principal": "1-0,5 mm, arena gruesa",
                                    "Descripción_de_clastos": "Hay clastos de volcanismo indiferenciado y restos de cuarzo  ",
                                    "Presencia_de_materia_orgánica_húmica": "Moderada",
                                    "FACTORES_ANTROPOGÉNICOS_QUE_PODRÍAN_ALTERAR_LA_MUESTRA": "Zona de sondajes inactivos",
                                    "OTRAS_OBSERVACIONES": "No se observan afloramientos Drenaje de muy baja pendiente Moderada  Mineralógicamente se observa que los clastos contienen cuarzo, óxidos de cobre, crisocola, atacamita",
                                    "F17": None,
                                    "CTOTAL___": 0.34,
                                    "STOTAL__": 0.05,
                                    "SiO2": 54.74,
                                    "Al2O3": 16.32,
                                    "Fe2O3": 11.44,
                                    "MgO": 2.2,
                                    "CaO": 2.84,
                                    "Na2O": 2.14,
                                    "K2O": 2.04,
                                    "TiO2": 1.38,
                                    "P2O5": 0.22,
                                    "MnO": 0.14,
                                    "Cr2O3": "0,009",
                                    "LOI": 6.3,
                                    "Suma": 99.72,
                                    "Sc": 13,
                                    "Ba": 718,
                                    "Be": "2",
                                    "Co": 24.2,
                                    "Cs": 8.5,
                                    "Ga": 22.7,
                                    "Hf": 6.8,
                                    "Nb": 11.3,
                                    "Rb": 75.9,
                                    "Sn": "3",
                                    "Sr": 389.9,
                                    "Ta": 0.8,
                                    "Th": 12.6,
                                    "U": 2.6,
                                    "V": 263,
                                    "W": 1.2,
                                    "Zr": 244.2,
                                    "Y": 16.3,
                                    "La": 35.3,
                                    "Ce": 67.5,
                                    "Pr": 8.25,
                                    "Nd": 31,
                                    "Sm": 5.43,
                                    "Eu": 1.25,
                                    "Gd": 4.11,
                                    "Tb": 0.52,
                                    "Dy": 3.35,
                                    "Ho": 0.54,
                                    "Er": 1.67,
                                    "Tm": 0.24,
                                    "Yb": 1.46,
                                    "Lu": 0.25,
                                    "Mo": 0.6,
                                    "Cu": 42.1,
                                    "Pb": 14.2,
                                    "Zn": 73,
                                    "Ni": 15.9,
                                    "As_": 13.1,
                                    "Cd": "0,2",
                                    "Sb": "0,3",
                                    "Bi": "0,3",
                                    "Ag": "<0,1",
                                    "Au": "1,4",
                                    "Hg": "0,02",
                                    "Tl": "0,3",
                                    "Se": "<0,5",
                                    "Te_ppm": "sin datos",
                                    "B_ppm": "sin datos",
                                    "geochemistry_published": True,
                                    "index_right": 7,
                                    "OBJECTID_right": 8,
                                    "COD_CUEN": "012",
                                    "COD_SUBC": "0121",
                                    "COD_SSUBC": "01210",
                                    "NOM_SSUBC": "Rio Lluta entre Quebrada Socoroma y Quebrada Poconchile",
                                    "Shape_Leng": 153745.859591,
                                    "Shape__Area": 884354360.6286621,
                                    "Shape__Length": 153745.85959075263,
                                    "COD_SSUBC_measure": "01210"
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                    -69.67635579706479,
                                    -18.300213565109562
                                    ]
                                }
                                }
                        }
                    }
                }
            }
         )
def prospectivity_map_measurement(id: int):
    gdf = gpd.read_parquet("data/processed/prospectivity_map.parquet")
    measurement = gdf[gdf["OBJECTID_left"] == id]
    if measurement.empty:
        raise HTTPException(status_code=404, detail="Measurement not found")
    measurement = measurement.to_crs(4326)
    feature = json.loads(measurement.to_json())["features"][0]
    return feature

@app.post("/predict-sample-prospectivity",
            description="Predict mineral prospectivity from a geochemical measurement.",
            tags=["Predict Prospectivity"],
            response_model=PredictResponse
          )
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