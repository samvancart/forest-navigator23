import xarray as xr
import numpy as np
import pandas as pd
import math
from functools import partial

import utility_functions as uf


# NETCDF FOR EACH VARIABLE
netcdfs = []

def _preprocess_coords(x, coords, start_year = 2002, end_year = 2021):
    data = x.where((x['time.year'] >= start_year) & (x['time.year'] <= end_year), drop=True)
    
    # FILTER OUT UNNECESSARY COORDINATES
    data = data.sel(lat = coords['lat'].to_xarray(), lon = coords['lon'].to_xarray(), method = 'nearest')

    return data

def _preprocess_1_day_bounds(x, lon_bnds, lat_bnds, year, month=1, day=1):

    # Remove unwanted data by coordinates
    ds = x.where((x.latitude<=lat_bnds[1]) & (x.latitude>=lat_bnds[0]) & (x.longitude<=lon_bnds[1]) & (x.longitude>=lon_bnds[0]), drop=True)
    
    # 1 day of data to get all coordinates
    data = ds.where((ds['time.year']==year) & (ds['time.month']==month) & (ds['time.day']==day), drop=True)
    return data


def _preprocess_coords_aggregate(x, coords, function, start_year = 2002, end_year = 2021):
    ds = x.where((x['time.year'] > start_year) & (x['time.year'] < end_year), drop=True)
    
    # ONE INDEX WITH ONLY THE NECESSARY COORDINATES
    data = ds.sel(latitude = coords['lat'].to_xarray(), longitude = coords['lon'].to_xarray(), method = 'nearest')
    
    var = list(data.keys())[0]
    data = function(data, var)

    return data

def _preprocess_bounds_aggregate(x, lon_bnds, lat_bnds, function, start_year = 2002, end_year = 2021):
    ds = x.where((x['time.year'] > start_year) & (x['time.year'] < end_year), drop=True)

    # Remove unwanted data by coordinates
    data = ds.where((ds.latitude<=lat_bnds[1]) & (ds.latitude>=lat_bnds[0]) & (ds.longitude<=lon_bnds[1]) & (ds.longitude>=lon_bnds[0]), drop=True)

    var = list(data.keys())[0]
    data = function(data, var)

    return data


def get_means(data, var, time='1m'):
    y = data[var]
    data_arr = y.resample(time=time).mean()
    data = data_arr.to_dataset()
    return data

def get_sums(data, var, time='1m'):
    y = data[var]
    data_arr = y.resample(time=time).sum()
    data = data_arr.to_dataset()
    return data

def get_frost_days(data, var, time='1m'):
    data = data.assign(frost_days = lambda x: x[var] < 0)
    return get_sums(data, 'frost_days', time)

def get_par(data, var, time='1m'):
    # CONVERT DAILY qq TO rss 
    data = data.assign(rss = lambda x: x[var] *0.0864)
    # CONVERT DAILY rss TO MONTHLY MEANS
    data = get_means(data, 'rss', time)
    # CONVERT rss TO par
    data = data.assign(par = lambda x: x['rss'] *0.44*4.56)
    return data

def get_vpd(df, tair, rh):
    tair = np.array(df[tair])
    rh = np.array(df[rh])
    applyvpd = np.vectorize(calculate_vpd_from_np_arrays)
    vpd = applyvpd(tair,rh)
    df = df.assign(vpd=vpd)
    return df

def calculate_vpd_from_np_arrays(tair,rh):
    svp = 610.7 * 10**(7.5*tair/(237.3+tair))
    vpd = svp * (1-(rh/100)) / 1000
    return vpd


# GET ONLY NECESSARY COORDS
def process_vars2(vars, coords):
# PROCESS EACH VAR
    for v in vars:
        print(f'Processing variable {v[0]}...')
        var = v[0]
        function = v[1]
        path = f"data/netcdf/vars/{var}/"


        partial_func = partial(_preprocess_coords_aggregate, coords=coords, function=function)

        # OPEN ALL DATASETS AT ONCE
        data = xr.open_mfdataset(
            f"{path}*.nc", combine='nested', concat_dim='time', preprocess=partial_func, chunks='auto'
        )

        netcdfs.append(data)
        print(f'{v[0]} done.')
        
    return netcdfs

# COMBINE ALL VARS INTO ONE NETCDF WITH COORDINATES WITHIN BOUNDS
def process_vars_and_aggregate(vars, lat_bnds, lon_bnds, var_path):
# PROCESS EACH VAR
    for v in vars:
        print(f'Processing variable {v[0]}...')
        var = v[0]
        function = v[1]
        path = f"{var_path}/{var}/"

        partial_func = partial(_preprocess_bounds_aggregate, lat_bnds=lat_bnds, lon_bnds=lon_bnds, function=function)

        # OPEN ALL DATASETS AT ONCE
        data = xr.open_mfdataset(
            f"{path}*.nc", combine='nested', concat_dim='time', preprocess=partial_func, chunks='auto'
        )

        data = uf.round_coords(data, lat = 'latitude', lon = 'longitude')

        netcdfs.append(data)
        print(f'{v[0]} done.')

    return netcdfs



# GET ONLY NECESSARY COORDS
def process_vars(vars, var_path, coords, start_year=2002, end_year=2021):
# PROCESS EACH VAR
    for v in vars:
        print(f'Processing variable {v}...')
        path = f"{var_path}{v}/"

        # OPEN ALL DATASETS AT ONCE
        data = xr.open_mfdataset(
            f"{path}*.nc", combine='nested', concat_dim='time', chunks='auto'
        )

        # FILTER
        data = data.where((data['time.year'] >= start_year) & (data['time.year'] <= end_year), drop=True)
        data = data.sel( lat = coords['lat'].to_xarray(), lon = coords['lon'].to_xarray(), method = 'nearest')

        netcdfs.append(data)
        print(f'{v} done.')
        
    return netcdfs


def var_to_prebas_tran(df,var):
    var_df = df[['time', 'climID', var]]
    var_df = var_df.pivot(index='climID', columns='time', values=var)
    var_df = var_df.rename(columns={x:y for x,y in zip(var_df.columns, range(1,len(var_df.columns)+1))})
    var_df = var_df.add_prefix('V')
    return var_df

def kelvin_to_celsius(df, vars):
    for var in vars:
        df[var] = df[var]-273.15
    return df

def prebas_out_var_to_long_form(df, var, speciesID=2, nyears=38):
    
    # DROP THINNING INFO (CHECK YEARS)
    df.drop(df.iloc[:, nyears+1:], inplace=True, axis=1)
    # DROP FIRST COLUMN
    df.drop(df.iloc[:,:1], inplace=True, axis=1)
    # STRIP COLUMN NAMES FROM X1.stand to X1
    df.rename(columns=lambda x: x.split('.')[0].strip(), inplace=True)
    df['climID'] = df.index+1
    df['speciesID'] = speciesID
    df = pd.wide_to_long(df, stubnames='X', i=['climID', 'speciesID'], j='year')
    df.rename(columns={'X': var}, inplace=True)
    return df


# PARAMETERS A AND B FOR 
# Saxton Equations to determine soil physical properties
# FROM: https://www.researchgate.net/publication/259198849_Saxton_Equations_to_determine_soil_physical_properties_in_MSExcel_format
def get_soil_param_a(sand, clay):
    result = math.exp(-4.396-0.0715*clay-0.000488*sand**2-0.00004285*sand**2*clay)
    return result

def get_soil_param_b(sand, clay):
    result = -3.14-0.00222*clay**2-0.00003484*sand**2*clay
    return result

def get_wilting_point(a, b):
    result = (15/a)**(1/b) * 1000
    return result

def get_field_capacity(a, b):
    result = (0.33333/a)**(1/b) * 1000
    return result