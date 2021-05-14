#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:44:46 2021

@author: julianamelara
"""
#import modules pandas, numpy, geopandas, and requests

import pandas as pd 
import numpy as np
import geopandas 
import requests


#read csv into file under variable ny

ny = pd.read_csv("COVID-19_Case_Geography_NY.csv", dtype = str)

#drop any columns with missing variables using .dropna() on ny

ny.dropna()


#drop all columns except 'case_month', 'res_state', 'state_fips_code', 
#'res_county', 'county_fips_code', 'age_group', 'exposure_yn', 'current_status', 
#'death_yn'

drop = ["sex", "race", "ethnicity", "case_positive_specimen_interval" , 
           "case_onset_interval", "process" , "symptom_status" , "hosp_yn" ,
           "icu_yn" , "underlying_conditions_yn" , "exposure_yn" , "death_yn"]

#drop without creating new variable by including inplace = True 

ny.drop(drop, axis = "columns" , inplace =True)

ny.to_csv("COVID-19_Case_Geography_NY_CLEAN.csv")
#%%

#build into dataframe 

ny = pd.DataFrame(ny)

#rename county_fips_code column to "GEOID" for ease with later join

ny = ny.rename({"county_fips_code" : "GEOID"} , axis = "columns" , inplace = False)

#set index to "GEOID" 

ny = ny.set_index("GEOID")

#drop any rows or columns with missing data 

ny = ny.dropna()

#sort the dataframe index 

ny = ny.sort_index()

#%%
#query the laboratory confirmed cases to gather the COVID positive cases 

query = ny.query("current_status ==  'Laboratory - confirmed case'")

#group that query by GEOID and age_group and then call the .size() 
#function to get the number of infections per age group per GEOID 

grouped = ny.groupby(["GEOID" , "age_group"]).size()

#call the unstack function to get a table
 
unstack = grouped.unstack()

#read unstack into a dataframe called new 

new = pd.DataFrame(unstack)

#drop the "Missing" column from new 

new = new.drop("Missing" , axis = "columns")

#set the variables in new to integers using the .astype() method call

new = new.astype(int)

#create a new column in new called "18+ years" that combines the 0-17 years, 18-49 years, and 50-64 years
#columns of new

new["18+ years"] = new["0 - 17 years"] + new["18 to 49 years"] + new["50 to 64 years"]

#create a list called dropping that includes the columns that were combined above 

dropping = ["0 - 17 years" , "18 to 49 years" , "50 to 64 years"]

#then drop those columns after creating the new column "18+ years"

new = new.drop(dropping, axis = "columns")


#read in vaccination data csv 

ny_vac = pd.read_csv("county_level_vaccination_data_for_new_york_may.csv")

#create new dataframe called vac that reads in the csv data 

vac = pd.DataFrame(ny_vac)

#set the index of vac to People Full Vaccinated - Resident 

vac = vac.set_index("People Fully Vaccinated - Resident")

#rename the County column of vac to NAME 

vac = vac.rename( {"County" : "NAME"}, axis = "columns" , inplace = False)

 #%%    
#set the STATEFP, COUNTYFP, and GEOID columns to strings using a dictionary called fips 
#before reading in the next csv

fips = {"STATEFP" : str, "COUNTYFP" : str, "GEOID" : str}   
   
#read in the tigerline us county csv with the argumenent dtype = fips 

states = pd.read_csv("tl_2019_us_county.csv", dtype = fips)

#query the dataframe with whatever state fips code you would like to analyze 

df = states.query("STATEFP == '36'")

#use the variable join to merge vac onto df on =  NAME, how = left, validate = 1:1, indicator = True

join = vac.merge(df, on = "NAME" ,
                     how = "left" , 
                     validate = "1:1",
                     indicator = True)

#set the index of join to GEOID 

join = join.set_index("GEOID")

#drop the merge column

join = join.drop("_merge" , axis = "columns")

#%%
#read the tigerline county zip file in using the geopandas read_file method 

county = geopandas.read_file("zip://tl_2020_us_county.zip")

#drop the geometry column from county 

county.drop("geometry" , axis = "columns" , inplace = True)

#create a new variable called vaccine query that queries the state fips code for the 
#state of interest

vaccine_query = county.query("STATEFP == '36'")

#create a new variable called vaccine that joins vaccine_query onto join 
#how = right on = GEOID validate = 1:m indicator = False 

vaccine  = vaccine_query.merge(join, how = "right" , on = "GEOID" ,  validate = "1:m" , indicator = False)


#%%
#clean up the file by creating a lsit of duplicate columns called rid 

rid = ['COUNTYFP_y',
       'COUNTYNS_y', 'NAMELSAD_y', 'LSAD_y', 'CLASSFP_y', 'MTFCC_y', 'CSAFP_y',
       'CBSAFP_y', 'METDIVFP_y', 'FUNCSTAT_y', 'ALAND_y', 'AWATER_y',
       'INTPTLAT_y', 'INTPTLON_y']

#drop rid from vaccine_clean

vaccine_clean = vaccine.drop(rid, axis = "columns")

#set index of vaccine clean to GEOID 

vaccine_clean = vaccine_clean.set_index("GEOID")
#%%
#query the census udner the variable call for county name and the census code 
#for population B02001_001E

call = "NAME,B02001_001E"

#create a variable called api that includes a link to the census api 

api = "https://api.census.gov/data/2018/acs/acs5"

#create a variable called for clause that is equal to "county:*"

for_clause = "county:*"

#create a variable in_clause that is equal to "state:#" -insert state fips code 

in_clause = "state:36"

#create a variable called key_value that includes your api key 

key_value = "8b426daac1c3a5b1421c36d70788d666054f4087"

#create a variable called result that builds a dictionary to query the census 

result = {'get':call, 'for':for_clause, 'in':in_clause,'key':key_value}

#create a variable called response that uses the .get() method to take the arguments api and result
response = requests.get(api, result)

#create an if statement to determine the success of the api call 
#set if response.status_code == 200 to determine the http success 

if response.status_code == 200:
    print( 'status:', response.status_code)
    print("Success")   
else:
    print(response.status_code)
    print(response.text), 
    assert False

#create a variable called row_list that is equal to calling .json() on response

row_list = response.json()
    
#create a variable colnames that is equal to row_list[0]

colnames = row_list[0]

#create a variable datarows that is equal to rowlist[1:]

datarows = row_list[1:]
#%%
#create a variable called call that reads into a dataframe columns = colnames and data = datarows 

call = pd.DataFrame(columns = colnames, data = datarows)

#rename the county column in call to COUNTYFP

call = call.rename({"county" : "COUNTYFP"} , axis = "columns" , inplace = False)

#create a new column in call GEOID that is equal to the sum of the state column 
#of call and the COUNTY FP column of call

call["GEOID"] = call["state"] + call["COUNTYFP"]

#set the index of call to GEOID 

call = call.set_index("GEOID")

#set the B02001_001E column of vaccine_clean to the B02001_001E column of call

vaccine_clean["B02001_001E"] = call["B02001_001E"]

#%%

#create a variable called full_join that merges vaccine_clean onto new 
#on GEOID how outer validate 1:m indicator = False 

full_join = vaccine_clean.merge(new, on = "GEOID" , 
                       how = "outer", 
                       validate = "1:m" , 
                       indicator = False)
#%%

#set the B02001_001E of full join equal to a numeric using the .to_numeric() method

full_join['B02001_001E'] = pd.to_numeric(full_join['B02001_001E'])

#set herd equal to the following columns of full join 
#["65+ years"] ["18+ years"] ["People 18+ Fully Vaccinated - Resident"] ["People 65+ Fully Vaccinated - Resident"]

herd = full_join["65+ years"] + full_join["18+ years"] + full_join["People 18+ Fully Vaccinated - Resident"] + full_join["People 65+ Fully Vaccinated - Resident"]

#create a new column in full_join called "immunity" which is equal to herd/ the B02001_001E column of full_join

full_join["immunity"] = herd/full_join["B02001_001E"]

#%%
#create a new variable geo to read the tigerline zip fule into the scirpt using geopandas .read_file()

geo = geopandas.read_file("zip://tl_2020_us_county.zip")

#query geo for the state fips code of interest 

query = geo.query("STATEFP == '36'")
#%%
#create a new variable joined to merge query onto full join 
#how = left on = GEOID validate = 1:1 indicator = False 

joined  = query.merge(full_join, how = "left" , on = "GEOID" , 
                      validate = "1:1" , indicator = False)

#use the .to_file() method on joined to export joined to a geopackage using the driver GPKG

joined.to_file("new_york.gpkg" , driver = "GPKG")



