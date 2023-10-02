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

def rename_netcdf_longFormat_coords(data, coord_names):
    dim_coords = list(data.coords)
    for coord_name in coord_names:
        if dim_coords.count(coord_name) > 0:
            data = data.rename({coord_name : coord_name[0:3]})
    return data

def main():

    start_year = 1979
    end_year = 2100
    lat = "latitud"
    lon = "lon"
    vars = ["pr","rsds","tas","tasmax","tasmin"]
    vars = ["pr"]

    coords_path = f"data/csv/site/coords_to_get.csv"
    coords = pd.read_csv(coords_path)

    netcdf_path = f"data/netcdf/CHELSA_EU/"
    combined_path = f"{netcdf_path}combined/"

    # data = xr.open_dataset(f"{netcdf_path}pr/chelsa_EU_pr_300arcsec_daily197901.nc")
    data = xr.open_dataset("C:/Users/samu/Documents/yucatrote/projects/sweden-may23/data/netcdf/vars/tg/tg_ens_mean_0.1deg_reg_1995-2010_v27.0e.nc")
    # data = vh.process_vars(vars,netcdf_path,coords,start_year,end_year)
    data = rename_netcdf_longFormat_coords(data, ["latitude","longitude"])
    # data = xr.open_mfdataset(
    #         f"{combined_path}*.nc", compat="override",chunks='auto'
    #     )
    print(data)

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
