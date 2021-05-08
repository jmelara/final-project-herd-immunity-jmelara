import pandas as pd 

#read csv into file under variable ny
ny = pd.read_csv("COVID-19_Case_Geography_NY.csv", dtype = str)

#print columns
print("Columns" , list(ny.columns))

#drop any columns with missing variables using .dropna() on ny
ny.dropna()

trim = ny.drop("Probable Case", axis ="index")


#drop all columns except 'case_month', 'res_state', 'state_fips_code', 'res_county', 'county_fips_code', 'age_group', 'exposure_yn', 'current_status', 'death_yn'
drop = ["sex", "race", "ethnicity", "case_positive_specimen_interval" , 
           "case_onset_interval", "process" , "symptom_status" , "hosp_yn" ,
           "icu_yn" , "underlying_conditions_yn" , "exposure_yn" , "death_yn"]

#drop without creating new variable by including inplace = True 
ny.drop(drop, axis = "columns" , inplace =True)

ny.to_csv("COVID-19_Case_Geography_NY_CLEAN.csv")



#need to drop Probable Case in Rows 
#more_drop = ["Probable Case"]
#arizona.drop(more_drop, axis = "index")

#need to drop rows and columns that have blank data (thought .dropna() did that)