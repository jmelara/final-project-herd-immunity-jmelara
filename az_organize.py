#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:56:31 2021

@author: julianamelara
"""

import pandas as pd 
import numpy as np

#read csv into file under variable arizona 
arizona = pd.read_csv("COVID-19_Case_Geography_AZ_test.csv", dtype = str)

#print columns
print("Columns" , list(arizona.columns))


#drop all columns except 'case_month', 'res_state', 'state_fips_code', 'res_county', 'county_fips_code', 'age_group', 'exposure_yn', 'current_status', 'death_yn'
drop = ["sex", "race", "ethnicity", "case_positive_specimen_interval" , 
           "case_onset_interval", "process" , "symptom_status" , "hosp_yn" ,
           "icu_yn" , "underlying_conditions_yn" , "exposure_yn" , "death_yn"]

#drop without creating new variable by including inplace = True 
arizona.drop(drop, axis = "columns" , inplace =True)


arizona.to_csv("COVID-19_Case_Geography_AZ_CLEAN_test.csv")

az = pd.DataFrame(arizona)
az = az.rename({"county_fips_code" : "GEOID"} , axis = "columns" , inplace = False)
az = az.set_index("case_month")
az = az.dropna()
az = az.sort_index()

age_17 = az.query("age_group == '0 - 17 years'")
age_18 = az.query("age_group == '18 - 49 years'")
age_50 = az.query("age_group == '50 - 64 years'")
age_65 = az.query("age_group == '65+ years'")
query = az.query("current_status ==  'Laboratory - confirmed case'")



#grouped = az.groupby(["GEOID" , "current_status" , "age_17" ,"age_18" , "age_50" , "age_65"])

#grouped = az.groupby(["age_group" , "GEOID" , ]).size()

#unstack = grouped.unstack()










