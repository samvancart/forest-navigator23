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

def prebas_out_var_to_long_form(var, speciesID=2, nyears=38):
    df_path = f'data/csv/prebas_out/{var}.csv'
    df = pd.read_csv(df_path)
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

def join_dataframes(vars):
    dfs = []
    new = pd.DataFrame()
    for i, var in enumerate(vars):
        df = prebas_out_var_to_long_form(var)
        dfs.append(df)
        if i == 0:
            new = dfs[0]
            dfs=[]
        else:
            new = new.join(dfs[0])
            dfs = []

    return new


def main():
    # vars = ['ba','dbh','gross_growth','h','n','npp','v']
    # new = join_dataframes(vars)
    # print(new)
    # path = f'data/csv/prebas_out/prebas_out_vars.csv'
    # uf.write_df_to_csv(new, path, index=True)

    prebas_path = f'data/csv/climate/historical_climate_data.csv'
    df = pd.read_csv(prebas_path, parse_dates=['time'])
    print(df)
    
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
    # df = kelvin_to_celsius(df, ['tair', 't_max', 't_min'])
    # # df['CO2'] = 380
    # df = df.drop(['t_min', 't_max', 'lat', 'lon'], axis=1)
    # df = df.rename(columns={"par":"PAR","tair":"TAir","vpd":"VPD","precip":"Precip"})
    # cols = ["time","climID","PAR","TAir","VPD","Precip","CO2"]
    # df = uf.rearrange_df(df, cols)
    # path = f'data/csv/climate/historical_prebas.csv'
    # uf.write_df_to_csv(df, path)

    # # WRITE TRAN FILES
    # prebas_path = f'data/csv/climate/historical_prebas.csv'
    # df = pd.read_csv(prebas_path, parse_dates=['time'])
    # vars = ['PAR', 'TAir', 'Precip', 'VPD', 'CO2']
    # for v in vars:
    #     path = f'data/csv/climate/tran/{v}_tran.csv'
    #     var_tran = var_to_prebas_tran(df, v)
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
