import xarray as xr
import pandas as pd
import numpy as np

import variable_handler as vh
import utility_functions as uf


def combine_by_nearest_coords( 
        netcdf_path, 
        coords_path,
        pre_function,
        vars,
        round_decimals = 2 ,
        start_year = 2002, 
        end_year = 2021,
        lon = "longitude",
        lat="latitude", 
        coords_lon="longitude",
        coords_lat="latitude"
                            ):
    
    coords = pd.read_csv(coords_path)

    data = vh.process_vars(pre_function, vars, netcdf_path, coords, round_decimals, start_year,end_year,
                           lon=lon,lat=lat,coords_lat=coords_lat,coords_lon=coords_lon)

    data = xr.merge(data)

    return(data)


def combine_by_bounds( 
        netcdf_path, 
        coords_path,
        pre_function,
        vars,
        bnds,
        round_decimals = 2 ,
        start_year = 2002, 
        end_year = 2021,
        lon = "longitude",
        lat="latitude", 
        coords_lon="longitude",
        coords_lat="latitude",
                            ):
    
    coords = pd.read_csv(coords_path)
    lat_bnds, lon_bnds = bnds[0], bnds[1]
    
    data = vh.process_vars(pre_function, vars, netcdf_path, coords,round_decimals, start_year,end_year,
                           lon=lon,lat=lat,coords_lat=coords_lat,coords_lon=coords_lon,lon_bnds=lon_bnds,lat_bnds=lat_bnds)

    data = xr.merge(data)

    return(data)


def write_file(path, data):
    print(f"Writing to {path}...")
    xr.save_mfdataset(datasets=[data],paths=[path])
    print(f"Done.")


def get_chelsa(coords_path, pre_function):

    netcdf_path = f"data/netcdf/CHELSA_EU/"

    start_year = 1979
    end_year = 2100
    round_decimals = 3
    pre_function = pre_function
    lat = "lat"
    lon = "lon"
    vars = ["pr","rsds","tas","tasmax","tasmin"]
    # vars = ["tasmin"]

    data = combine_by_nearest_coords(
        netcdf_path=netcdf_path, 
        coords_path=coords_path,
        pre_function=pre_function,
        vars=vars,
        round_decimals = round_decimals,
        start_year = start_year, 
        end_year = end_year,
        lon=lon,
        lat=lat, 
        coords_lon=lon,
        coords_lat=lat)


    return data

def get_eobs(coords_path, pre_function):
    netcdf_path = f"C:/Users/samu/Documents/yucatrote/projects/sweden-may23/data/netcdf/vars/"

    start_year = 1979
    end_year = 2100
    round_decimals = 3
    pre_function = pre_function
    lat = "latitude"
    lon = "longitude"
    coords_lon = "lon"
    coords_lat = "lat"
    vars = ["hu","qq","rr","tg","tn", "tx"]
    # vars = ["hu","qq"]

    data = combine_by_nearest_coords(
        netcdf_path=netcdf_path, 
        coords_path=coords_path,
        pre_function=pre_function,
        vars=vars,
        round_decimals = round_decimals,
        start_year = start_year, 
        end_year = end_year,
        lon=lon,
        lat=lat, 
        coords_lon=coords_lon,
        coords_lat=coords_lat)


    return data

def get_eobs_bounds(coords_path, pre_function):
    netcdf_path = f"C:/Users/samu/Documents/yucatrote/projects/sweden-may23/data/netcdf/vars/"
    coords = pd.read_csv(coords_path)

    start_year = 1979
    end_year = 2100
    round_decimals = 3
    pre_function = pre_function
    lat = "latitude"
    lon = "longitude"
    coords_lon = "lon"
    coords_lat = "lat"
    vars = ["hu","qq","rr","tg","tn", "tx"]
    # vars = ["hu","qq"]

    bnds = uf.get_bounds(coords)

    data = combine_by_bounds(
        netcdf_path=netcdf_path, 
        coords_path=coords_path,
        pre_function=pre_function,
        vars=vars,
        bnds = bnds,
        round_decimals = round_decimals,
        start_year = start_year, 
        end_year = end_year,
        coords_lon=coords_lon,
        coords_lat=coords_lat)


    return data