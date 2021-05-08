#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:44:46 2021

@author: julianamelara
"""

import geopandas 
import pandas as pd 

states = geopandas.read_file("tl_2019_us_county.csv")

df = pd.DataFrame(states)
df = df.set_index("STATEFP")
df = df.sort_index()
df = df.filter( like = "04" , axis = "index")
df = df.set_index("NAME")
print(df)

