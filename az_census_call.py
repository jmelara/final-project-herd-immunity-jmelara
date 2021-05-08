#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:44:46 2021

@author: julianamelara
"""

import pandas as pd 
import requests 

earnings = "NAME,B20002_001E"

api = "https://api.census.gov/data/2018/acs/acs5"

for_clause = "county:*"

in_clause = "state:04"

key_value = "8b426daac1c3a5b1421c36d70788d666054f4087"

earnings = {'get':earnings, 'for':for_clause, 'in':in_clause,'key':key_value}

response = requests.get(api, earnings)

if response.status_code == 200:
    print( 'status:', response.status_code)
    print("Success")   
else:
    print(response.status_code)
    print(response.text), 
    assert False
    
    
row_list = response.json()
    
colnames = row_list[0]
datarows = row_list[1:]

earnings = pd.DataFrame(columns = colnames, data = datarows)

earnings.to_csv("arizona_census.csv" , index = False)