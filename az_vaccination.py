#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:44:46 2021

@author: julianamelara
"""

import pandas as pd 


az_vac = pd.read_csv("county_level_vaccination_data_for_arizona_may.csv", dtype = str)

vac = pd.DataFrame(az_vac)
vac = vac.set_index("People Fully Vaccinated - Resident")
vac = vac.rename( {"County" : "NAME"}, axis = "columns" , inplace = False)
vac = vac.set_index("NAME")

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
