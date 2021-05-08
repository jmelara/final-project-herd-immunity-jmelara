#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:44:46 2021

@author: julianamelara
"""
#import modules pandas and numpy 

import pandas as pd 
import numpy as np

#read csv into file under variable arizona 

arizona = pd.read_csv("COVID-19_Case_Geography_AZ_test.csv", dtype = str)

#print columns

#print("Columns" , list(arizona.columns))


#drop all columns except 'case_month', 'res_state', 'state_fips_code', 
#'res_county', 'county_fips_code', 'age_group', 'exposure_yn', 'current_status',
#'death_yn'

drop = ["sex", "race", "ethnicity", "case_positive_specimen_interval" , 
           "case_onset_interval", "process" , "symptom_status" , "hosp_yn" ,
           "icu_yn" , "underlying_conditions_yn" , "exposure_yn" , "death_yn"]

#drop without creating new variable by including inplace = True 

arizona.drop(drop, axis = "columns" , inplace =True)

#write the clean file to csv

arizona.to_csv("COVID-19_Case_Geography_AZ_CLEAN_test.csv")

#build dataframe 

ar = pd.DataFrame(arizona)

#rename county_fips_code column to "GEOID" for ease with later join

ar = ar.rename({"county_fips_code" : "GEOID"} , axis = "columns" , inplace = False)

#set index to "GEOID" 

ar = ar.set_index("GEOID")

#drop any rows or columns with missing data 

ar = ar.dropna()

#sort the dataframe index 

ar = ar.sort_index()


query = ar.query("current_status ==  'Laboratory - confirmed case'")

grouped = ar.groupby(["age_group" , "GEOID"]).size()

unstack = grouped.unstack()


#read vaccination csv

az_vac = pd.read_csv("county_level_vaccination_data_for_arizona_may.csv", dtype = str)

vac = pd.DataFrame(az_vac)
vac = vac.set_index("People Fully Vaccinated - Resident")
vac = vac.rename( {"County" : "NAME"}, axis = "columns" , inplace = False)
vac = vac.set_index("NAME")
print(vac)


import geopandas 

states = geopandas.read_file("tl_2019_us_county.csv")

df = pd.DataFrame(states)
df = df.set_index("STATEFP")
df = df.sort_index()
df = df.filter( like = "04" , axis = "index")
df = df.set_index("NAME")

join = vac.merge(df, on ="NAME",
                     how = "outer" , 
                     validate = "1:1",
                     indicator = True)
join = join.set_index("GEOID")


full_join = join.merge(ar, on = "GEOID" , 
                       how = "outer", 
                       validate = "1:m" , 
                       indicator = False)

query = full_join.query("current_status ==  'Laboratory - confirmed case'")

grouped = full_join.groupby([ "GEOID" , "age_group" , ]).size()

unstack = grouped.unstack()
print(unstack)

















   










