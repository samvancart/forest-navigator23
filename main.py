# E-OBS weather data to prebas format. Default time period = 1 month.
# Removes NaNs first and then creates dataframe with nearest climate ids
# INSTRUCTIONS
# Files for all the years of each e-obs variable should be in a folder with the variable's name eg. variable 'tg' in a folder called tg.
# Each step can be written as csv into a temp folder and read for the next step.
# CHECK NETCDF DIMENSIONS AFTER FIRST STEP, MIGHT BE TOO LARGE TO PROCESS FURTHER WITHOUT MODIFYING!

import xarray as xr
import pandas as pd
import numpy as np

import variable_handler as vh
import nan_handler as nh
import climate_id as clid
import utility_functions as uf
import netcdf as nc


def main():

    coords_path = f"data/csv/site/coords_to_get.csv"
    coords = pd.read_csv(coords_path)

    netcdf_path = f"data/netcdf/CHELSA_EU/"
    vars_path = f"{netcdf_path}combined/vars/"
    combined_path = f"{netcdf_path}combined/all/"
    file_name = "all_vars_test"

    start_year = 1979
    end_year = 2100
    round_decimals = 3
    pre_function = vh._preprocess_coords
    bnds = uf.get_bounds(coords)

    lat = "lat"
    lon = "lon"
    vars = ["pr","rsds","tas","tasmax","tasmin"]
    vars = ["tasmin"]

    # data = nc.combine_by_nearest_coords(
    #     netcdf_path=netcdf_path, 
    #     coords_path=coords_path,
    #     pre_function=pre_function,
    #     vars=vars,
    #     round_decimals = round_decimals,
    #     start_year = start_year, 
    #     end_year = end_year,
    #     lon=lon,
    #     lat=lat, 
    #     coords_lon=lon,
    #     coords_lat=lat)



     # STEP 1: PREPARE DF ACCORDING TO BOUNDS
    nan_removal_path = f"data/csv/climate/eobs_1979_2022_with_nans.csv"
    nans_removed_path = f"data/csv/climate/eobs_1979_2022_nans_removed.csv"

    # data_eobs_bnds = nc.get_eobs_bounds(coords_path=coords_path,pre_function=vh._preprocess_bounds)
    # print(data_eobs_bnds)
    # df = nh.get_nan_removal_df(data_eobs_bnds)
    # print(df)
    # uf.write_df_to_csv(df, nan_removal_path)

    # STEP 2: REMOVE ALL CLIMIDS WITH NANS 
    # df = nh.remove_nan_ids(nan_removal_path)
    df = pd.read_csv(nan_removal_path)
    # df = nh.remove_nans_from_df(df)
    # uf.write_df_to_csv(df, nans_removed_path)






    
    # data_chelsa = nc.get_chelsa(coords_path=coords_path, pre_function=pre_function)
    # print(data_chelsa)
    # path = f"{combined_path}chelsa_1979_2016_all_vars.nc"
    # nc.write_file(data=data_chelsa,path=path)

    # data_eobs = nc.get_eobs(coords_path=coords_path, pre_function=pre_function)
    # print(data_eobs)
    # path = f"C:/Users/samu/Documents/yucatrote/projects/sweden-may23/data/netcdf/combined/all/eobs_1979_2022_all_vars.nc"
    # nc.write_file(data=data_eobs,path=path)

    # data = xr.open_dataset(f"{netcdf_path}pr/chelsa_EU_pr_300arcsec_daily197901.nc")
    # data = xr.open_dataset(f"{netcdf_path}rsds/chelsa_EU_rsds_300arcsec_daily197901.nc")
    # data = xr.open_dataset(f"{combined_path}all_vars.nc")
    # print(data)
    # data = xr.open_dataset(f"{combined_path}all_vars_test.nc")
    # print(data)
    # data = xr.open_dataset("C:/Users/samu/Documents/yucatrote/projects/sweden-may23/data/netcdf/vars/tg/tg_ens_mean_0.1deg_reg_1995-2010_v27.0e.nc")
    # data = rename_netcdf_longFormat_coords(data, ["latitude","longitude"])
    


    # data = vh.process_vars(pre_function, vars, netcdf_path, coords, round_decimals, start_year,end_year,
    #                        lon=lon,lat=lat,coords_lat=lat,coords_lon=lon)
    
    # data = xr.merge(data)
    # print(data)
    # print(len(data.lat))
    # print(len(data.lon))
    # print(data.lat)
    # print(type(coords['lat'].tolist()))
    # print(len(data[0].lat))
    # print(len(data[0].lon))
    # print(data[0].lat)

    # for i,d in enumerate(data):
    #     print(i)
    #     print(d)
    

    # path = f"{combined_path}{vars[0]}_coords.nc"
    # print(f"Writing to {path}...")
    # data[0].to_netcdf(path)
    # print(f"{vars[0]} done.")

    # for d in enumerate(data):
    #     path = f"{combined_path}{vars[d[0]]}.nc"
    #     print(f"Writing to {path}")
    #     d[1].to_netcdf(path)
    #     print(f"{vars[d[0]]} done.")



    # data = xr.open_mfdataset(
    #         f"{combined_path}*.nc", compat='override', chunks='auto'
    #     )

    # print(data)
    # path = f"{combined_path}all_vars.nc"

    # print(f"Writing to {path}")
    # data.to_netcdf(path)
    # print(f"Done.")





    # # df_path = f'data/csv/climate/historical_prebas_sites.csv'
    # # df = pd.read_csv(df_path)
    # site_path = f'data/csv/site/plot_data.csv'
    # sites = pd.read_csv(site_path)
    # print(sites)
    # sites = sites.where(sites['domain'] == 'Picus_Prebas').dropna()
    # sites['PlgID'] = sites['PlgID'].astype(int)

    # # df = df.where(df['siteID'].isin(sites['PlgID'])).dropna()
    # # df[['siteID','climID']] = df[['siteID','climID']].astype(int)
    # # print(df)
    # # path = f'data/csv/climate/historical_only_prebas_picus_sites.csv'
    # # uf.write_df_to_csv(df, path, index=False)



    # soil_path = f'data/csv/soil/soil_data_ids_sorted.csv'
    # soil_df = pd.read_csv(soil_path)
    # new_soil_path = f'data/csv/soil/soil_data_wp_fc_gitlab_ids_sorted.csv'
    # new_soil_df = pd.read_csv(new_soil_path)
    # # soil_df = soil_df.sort_values(['climID'])
    # new_soil_df = new_soil_df.where(new_soil_df['siteID'].isin(sites['PlgID'])).dropna()
    # new_soil_df[['siteID','climID']] = new_soil_df[['siteID','climID']].astype(int)
    # print(new_soil_df)

    
    # print(soil_df[['climID','siteID','AWC','FC', 'WP']])
    # print(new_soil_df[['climID','siteID','AWC','FC', 'WP']])

    # new_soil_df.rename(columns={'PlgID':'siteID'},inplace=True)
    # new_soil_df = new_soil_df.merge(soil_df[['siteID','climID']])
    # new_soil_df = new_soil_df.sort_values(['climID'])
    # print(new_soil_df)
    # path = f'data/csv/soil/soil_data_wp_fc_gitlab_ids_sorted.csv'
    # uf.write_df_to_csv(new_soil_df, path, index=False)

    # print(soil_df[['WP','FC','AWC']])


    # # WILTING POINT AND FIELD CAPACITY FROM WILTING POINT 
    # soil_df['WP'] = soil_df.apply(lambda row: vh.get_wilting_point(vh.get_soil_param_a(row['sand'], row['clay']),vh.get_soil_param_b(row['sand'],row['clay'])),axis=1)
    # soil_df['FC'] = soil_df['AWC'] + soil_df['WP']
    # soil_from_fc_path = f'data/csv/soil/soil_data_ids_sorted.csv'
    # soil_from_fc_df = pd.read_csv(soil_from_fc_path)
    # # # WILTING POINT AND FIELD CAPACITY FROM FIELD CAPACITY
    # soil_from_fc_df['FC'] = soil_from_fc_df.apply(lambda row: vh.get_field_capacity(vh.get_soil_param_a(row['sand'], row['clay']),vh.get_soil_param_b(row['sand'],row['clay'])),axis=1) 
    # soil_from_fc_df['WP'] = soil_from_fc_df['FC'] - soil_from_fc_df['AWC']

    # print('soil from wp')
    # print(soil_df[['climID','siteID','AWC','FC', 'WP']])
    # print('soil from fc')
    # print(soil_from_fc_df[['climID','siteID','AWC','FC', 'WP']])
    # print('soil from gitlab')
    # print(new_soil_df[['climID','siteID','AWC','FC', 'WP']])
    
    # # print(soil_df)
    # print(soil_df[['WP','FC','AWC']])

    # CONCAT PREBAS OUT SPECIES FRAMES
    # pine_path = f'data/csv/prebas_out/out_pine.csv'
    # spruce_path = f'data/csv/prebas_out/out_spruce.csv'
    # birch_path = f'data/csv/prebas_out/out_birch.csv'
    # beech_path = f'data/csv/prebas_out/out_beech.csv'
    # pine = pd.read_csv(pine_path)
    # spruce = pd.read_csv(spruce_path)
    # birch = pd.read_csv(birch_path)
    # beech = pd.read_csv(beech_path)

    # df = pd.concat([pine,spruce,birch,beech])
    # print(df)

    # path = f'data/csv/prebas_out/prebas_out_all_species.csv'
    # uf.write_df_to_csv(df, path, index=False)


    # PREBAS OUTPUT TO DATAFRAME
    # df_path = f'data/csv/prebas_out/out_4_0_0.csv'
    # df = pd.read_csv(df_path)
    # vars = ['ba','dbh','gross_growth','h','n','npp','v']
    # dfs = []
    # for var in vars:
    #     df_path = f'data/csv/prebas_out/{var}.csv'
    #     df = pd.read_csv(df_path)
    #     # print(df)
    #     df = vh.prebas_out_var_to_long_form(df,var)
    #     dfs.append(df)

    # new = dfs[0].join(dfs[1:])
    # print(new)
    # new = new.melt(ignore_index=False)
    # print(new)


    # new = join_dataframes(vars)
    # print(new)
    # path = f'data/csv/prebas_out/prebas_out_vars.csv'
    # uf.write_df_to_csv(new, path, index=True)


    # CLIMATE DATA TO PREBAS
    # prebas_path = f'data/csv/climate/historical_climate_data.csv'
    # df = pd.read_csv(prebas_path, parse_dates=['time'])
    # print(df)

    # df = df.rename(columns={'PlgID' : 'siteID', 'XLON':'lon', 'YLAT':'lat', 'rsds':'qq', 'hurs': 'rh' , 'tas' : 'tair', 'prcp':'precip', 'tasmax': 't_max', 'tasmin': 't_min'})
    # # GET CO2 VALUES
    # co2_csv_path = f'data/csv/climate/co2_annual_1850_2021.csv'
    # co2_df = pd.read_csv(co2_csv_path)
    # co2_df = co2_df.loc[co2_df.year.isin(df.time.dt.year)]
    # co2_df.drop(co2_df.tail(4).index, inplace=True)
    # new = pd.DataFrame({'year':range(2018,2100)})
    # new['CO2'] = 405.22
    # co2_df = pd.concat([co2_df, new])
    # df['year'] = df.time.dt.year
    # df = df.merge(co2_df)
    # df.drop(['year'], axis=1)
    # # ASSIGN CLIMIDS
    # df['climID'] = df.groupby(['siteID']).ngroup()+1
    # # GET RSS FROM QQ
    # df = df.assign(rss = lambda x: x['qq'] *0.0864)
    # # GET PAR FROM RSS
    # df = df.assign(par = lambda x: x['rss'] *0.44*4.56)
    # # REARRANGE
    # df = df.drop(columns=['rh', 'rss'])
    # cols = ['time', 'siteID', 'climID', 'lat', 'lon', 'tair', 'precip', 'par', 'vpd', 't_min', 't_max', 'CO2']
    # df = uf.rearrange_df(df, cols)
    # # CONVERT [kg.m-2.s-1] to mm/d (86400 seconds in day)
    # df['precip'] = df['precip'] * 86400
    # # CONVERT TEMPERATURES FROM KELVIN TO CELSIUS
    # df = vh.kelvin_to_celsius(df, ['tair', 't_max', 't_min'])
    # # df['CO2'] = 380
    # df = df.drop(['t_min', 't_max', 'lat', 'lon'], axis=1)
    # df = df.rename(columns={"par":"PAR","tair":"TAir","vpd":"VPD","precip":"Precip"})
    # cols = ["time","siteID","climID","PAR","TAir","VPD","Precip","CO2"]
    # df = uf.rearrange_df(df, cols)
    # path = f'data/csv/climate/historical_prebas_sites.csv'
    # uf.write_df_to_csv(df, path)

    # WRITE TRAN FILES
    # prebas_path = f'data/csv/climate/historical_only_prebas_picus_sites.csv'
    # df = pd.read_csv(prebas_path, parse_dates=['time'])
    # vars = ['PAR', 'TAir', 'Precip', 'VPD', 'CO2']
    # for v in vars:
    #     path = f'data/csv/climate/tran/{v}_tran.csv'
    #     var_tran = vh.var_to_prebas_tran(df, v)
    #     print(var_tran)
    #     uf.write_df_to_csv(var_tran, path)

  

    # print(df)



    # df['DOY'] = df['time'].dt.dayofyear
    # CONVERT [kg.m-2.s-1] to mm/d (86400 seconds in day)
    # df['precip'] = df['precip'] * 86400
    # df['CO2'] = 380
    # df = df.drop(['t_min', 't_max', 'lat', 'lon', 'time'], axis=1)
    # df = df.rename(columns={"plotID":"siteID","par":"PAR","tair":"TAir","vpd":"VPD","precip":"Precip"})
    # cols = ["climID","DOY","PAR","TAir","VPD","Precip","CO2"]
    # df = uf.rearrange_df(df, cols)
    # prebas_example_path = f'data/csv/forest_nav_prebas_example.csv'
    # uf.write_df_to_csv(df, prebas_path)


    # df = df.rename(columns={'PlgID' : 'plotID', 'XLON':'lon', 'YLAT':'lat', 'rsds':'qq', 'tas' : 'tair', 'prcp':'precip', 'tasmax': 't_max', 'tasmin': 't_min'})
    # df = df.assign(rss = lambda x: x['qq'] *0.0864)
    # df = df.assign(par = lambda x: x['rss'] *0.44*4.56)
    # df = vh.get_vpd(df, 'tair', 'rh')
    # df = df.drop(columns=['rh', 'rss'])
    # cols = ['time', 'plotID', 'climID', 'lat', 'lon', 'tair', 'precip', 'par', 'vpd', 't_min', 't_max']
    # df = uf.rearrange_df(df, cols)
    # print(df)
    # uf.write_df_to_csv(df, prebas_path)
    # print(df.isnull().values.any())
    

       



    

    




if __name__ == '__main__':
    main()
