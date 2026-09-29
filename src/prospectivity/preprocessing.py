import numpy as np
import pandas as pd

# selecting measurement columns
measurements = [ 
        'CTOTAL___', 'STOTAL__', 'LOI', 'Suma', 
        'SiO2', 'Al2O3', 'Fe2O3', 'MgO', 'CaO', 'Na2O', 'K2O', 'TiO2', 'P2O5', 'MnO', 'Cr2O3',
        'Sc', 'Ba', 'Be', 'Co', 'Cs', 'Ga', 'Hf', 'Nb', 'Rb', 'Sn', 'Sr', 'Ta', 'Th', 'U', 'V', 'W', 'Zr', 'Y', 
        'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 
        'Mo', 'Cu', 'Pb', 'Zn', 'Ni', 'As_', 'Cd', 'Sb', 'Bi', 'Ag', 'Au', 'Hg', 'Tl', 'Se', 'Te_ppm', 'B_ppm'    
]

# standardize decimal separators
def replace_comma_dot(x):
    if isinstance(x, float):
        return x
    if x is None or x is pd.NA:
        return None
    x = x.replace(",,", ",")
    if "," in x and "." not in x:
        return x.replace(",", ".")
    if "." in x and "," not in x:
        return x
    if "." in x and "," in x:
        x_splited = x.split(",")
        if len(x_splited) > 2:
            x = f"{x_splited[0]},{''.join(x_splited[1:])}"
        return x.replace(".", "").replace(",", ".")
    return x

# remove extra zeros of a number
def less_than_remove_extra_zeros(x):
    if isinstance(x, str) and x[0] == "<":
        num = float(x[1:])
        return f"<{num}"
    return x

def formatting_numeric_values(df):
    df = df.copy()
    for measurement in measurements:
        # formatting
        df[measurement] = df[measurement].apply(replace_comma_dot).apply(less_than_remove_extra_zeros)
    return df

def initialize_categorical_columns(df):
    df = df.copy()
    categorical_columns = ['CTOTAL____isna', 'STOTAL___isna', 'SiO2_isna', 'Al2O3_isna', 'Fe2O3_isna', 'MgO_isna',
    'CaO_isna', 'Na2O_isna', 'K2O_isna', 'TiO2_isna', 'P2O5_isna', 'MnO_isna', 'Cr2O3_insufficient_sample', 'Cr2O3_<0.002',
    'LOI_isna', 'Suma_isna', 'Sc_isna', 'Ba_isna', 'Be_insufficient_sample', 'Be_<1.0', 'Co_isna', 'Cs_isna', 'Ga_isna', 'Hf_isna',
    'Nb_isna', 'Rb_isna', 'Sn_insufficient_sample', 'Sn_<1.0', 'Sr_isna', 'Ta_isna', 'Th_isna', 'U_isna', 'V_isna', 'W_isna',
    'Zr_isna', 'Y_isna', 'La_isna', 'Ce_isna', 'Pr_isna', 'Nd_isna', 'Sm_isna', 'Eu_isna', 'Gd_isna', 'Tb_isna', 'Dy_isna',
    'Ho_isna', 'Er_isna', 'Tm_isna', 'Yb_isna', 'Lu_isna', 'Mo_isna', 'Cu_isna', 'Pb_isna', 'Zn_isna', 'Ni_isna', 'As__isna',
    'Cd_insufficient_sample', 'Cd_<0.1', 'Sb_insufficient_sample', 'Sb_<0.1', 'Sb_>2000.0', 'Bi_insufficient_sample', 'Bi_<0.1',
    'Ag_insufficient_sample', 'Ag_<0.1', 'Au_insufficient_sample', 'Au_<0.5', 'Hg_insufficient_sample', 'Hg_<0.01',
    'Tl_insufficient_sample', 'Tl_<0.1', 'Se_insufficient_sample', 'Se_<0.5', 'Te_ppm_isna', 'Te_ppm_<0.2', 'B_ppm_isna', 
    'B_ppm_<3.0']
    for column in categorical_columns:
        if column not in df.columns:
            df[column] = False
    return df
    
def add_categorical_columns(df):
    df = df.copy()
    new_measurements_columns = {}
    for measurement in measurements:
        if not pd.api.types.is_float_dtype(df[measurement]):
            # define filters
            isna_filter = ((df[measurement].isna()) | 
            (df[measurement] == "sin datos") | 
            (df[measurement] == "-") | 
            (df[measurement] == "s/a"))
            insufficient_sample_filter = df[measurement] == "IS"
            starts_with_less_than_filter = ((df[measurement].str.startswith("<")) & 
            (~df[measurement].isna()))
            starts_with_more_than_filter = ((df[measurement].str.startswith(">")) & 
            (~df[measurement].isna()))
                
            # Add new categorical columns
            if isna_filter.sum() > 0:
                new_measurements_columns[f"{measurement}_isna"] = isna_filter
            if insufficient_sample_filter.sum() > 0:
                new_measurements_columns[f"{measurement}_insufficient_sample"] = insufficient_sample_filter
            if starts_with_less_than_filter.sum() >0:
                minimum = df[starts_with_less_than_filter].iloc[0][measurement]
                new_measurements_columns[f"{measurement}_{minimum}"] = starts_with_less_than_filter
            if starts_with_more_than_filter.sum() >0:
                maximum = df[starts_with_more_than_filter].iloc[0][measurement]
                new_measurements_columns[f"{measurement}_{maximum}"] = starts_with_more_than_filter
        else:
            isna_filter = df[measurement].isna()
            # Add new categorical columns
            if isna_filter.sum() > 0:
                new_measurements_columns[f"{measurement}_isna"] = isna_filter
    if new_measurements_columns:
        df = pd.concat([df, pd.DataFrame(new_measurements_columns, index=df.index)], axis=1)
    df = initialize_categorical_columns(df)
    return df

def get_median(df, measurement):
    df = df.copy()
    if not pd.api.types.is_float_dtype(df[measurement]):
        # define filters
        isna_filter = ((df[measurement].isna()) | 
        (df[measurement] == "sin datos") | 
        (df[measurement] == "-") | 
        (df[measurement] == "s/a"))
        insufficient_sample_filter = df[measurement] == "IS"
        starts_with_less_than_filter = ((df[measurement].str.startswith("<")) & 
        (~df[measurement].isna()))
        starts_with_more_than_filter = ((df[measurement].str.startswith(">")) & 
        (~df[measurement].isna()))
        # calculate the median
        median = pd.to_numeric(df[(
                (~isna_filter) &
                (~insufficient_sample_filter) & 
                (~starts_with_less_than_filter) &
                (~starts_with_more_than_filter))
                ][measurement]).median()
        return median
    else:
        return df[measurement].median()

def fill_with_median(df, df_for_median=None):
    df = df.copy()
    new_measurements_columns = {}
    for measurement in measurements:
        if not pd.api.types.is_float_dtype(df[measurement]):
            # define filters
            isna_filter = ((df[measurement].isna()) | 
            (df[measurement] == "sin datos") | 
            (df[measurement] == "-") | 
            (df[measurement] == "s/a"))
            insufficient_sample_filter = df[measurement] == "IS"
            starts_with_less_than_filter = ((df[measurement].str.startswith("<")) & 
            (~df[measurement].isna()))
            starts_with_more_than_filter = ((df[measurement].str.startswith(">")) & 
            (~df[measurement].isna()))
            if df_for_median is None:
                median = get_median(df, measurement)
            else:
                median = get_median(df_for_median, measurement)
            # assing the median
            df.loc[
                (isna_filter) |
                (insufficient_sample_filter) |
                (starts_with_less_than_filter) |
                (starts_with_more_than_filter)
                , [measurement]] = str(median)
            # convert to float
            df[measurement] = df[measurement].astype(float)
        else:
            if df_for_median is None:
                median = get_median(df, measurement)
            else:
                median = get_median(df_for_median, measurement)
            df[measurement] = df[measurement].fillna(median)
    return df

def logarithm_transformation(df):
    df = df.copy()
    measurements_without_loi = [ 
            'CTOTAL___', 'STOTAL__', 'Suma', 
            'SiO2', 'Al2O3', 'Fe2O3', 'MgO', 'CaO', 'Na2O', 'K2O', 'TiO2', 'P2O5', 'MnO', 'Cr2O3',
            'Sc', 'Ba', 'Be', 'Co', 'Cs', 'Ga', 'Hf', 'Nb', 'Rb', 'Sn', 'Sr', 'Ta', 'Th', 'U', 'V', 'W', 'Zr', 'Y', 
            'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 
            'Mo', 'Cu', 'Pb', 'Zn', 'Ni', 'As_', 'Cd', 'Sb', 'Bi', 'Ag', 'Au', 'Hg', 'Tl', 'Se', 'Te_ppm', 'B_ppm'    
    ]
    df[measurements_without_loi] = np.log1p(df[measurements_without_loi])
    return df
