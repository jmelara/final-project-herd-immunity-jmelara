#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 00:36:06 2021

@author: julianamelara
"""
#import pandas and geopandas 

import pandas as pd 
import geopandas 

#create a new variable called infection to read in the county level infection data

infection = pd.read_csv("county_level_new_york_infection_rate_may.csv")

#create a variable called organize to rename the County column of infection to NAME 

organize = infection.rename({"County" : "NAME"} , axis = "columns" , inplace = False)

#create a variable called mapping to read the tigerline county zip file in using 
#geopandas.read_file()

mapping = geopandas.read_file("zip://tl_2020_us_county.zip")

#create a variable called mapping to query the state fips code of interest 

adding = mapping.query("STATEFP == '36'")

#create rates to join adding onto organize 
#how = "left" , on = "NAME" , validate = "1:1" , indicator = False

rates = adding.merge(organize, how = "left" , on = "NAME" , 
                     validate = "1:1" , indicator = False)
#use the .to_file() method to write rates to a geopackage file using the driver GPKG

rates.to_file("new_york_rates.gpkg" , driver = "GPKG")
#end