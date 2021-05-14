# final-project-herd-immunity-jmelara
This repository captures county level progress toward "herd immunity" against COVID-19 throughout the United States. 
This analysis combines the number of infections per county since the COVID-19 outbreak in March 2020 with the number of vaccinations per county to estimate the 
percentage of the county that is "immune" against COVID. The analysis then compares the percentage of the county that is immune against current infection rates 
and trends. This analysis does not account for individuals that both had the vaccine and were previously infected with COVID-19 and also assumes that individuals were
vaccinated in thier county of residence. 

In order to run this analysis, certain data will need to be acquired. First, go to the Census and create an API key to query the Census https://api.census.gov/data/key_signup.html. 
Additionally, go to the Census website and download the most recent county level tigerline shape files with geometry https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
Next, go to the New York Times COVID-19 Daily tracker https://www.nytimes.com/interactive/2021/us/covid-cases.html. In order to obtain vaccination data, query the website 
for vaccinations and the site should link to the CDC Covid Data Tracker https://covid.cdc.gov/covid-data-tracker/#vaccinations. Once at this site, navigate to 
the "Vaccinations by County" tab. A map of the United States should appear. Query the map for total number of COVID cases, vaccination data, and 
levels of community transmission by state and county per month since the pandemic began. For the sake of this analysis, I pulled number of COVID cases per county 
since the pandemic onset in March of 2020, vaccination data per county since vaccine became available in January 2021, and infection rates as of the week of 
May 1st, 2021. 

This analysis also requires mapping in QGIS. Once the geopackages are written in spyder, open them in QGIS. To replicate this analysis - with the herd immunity geopackage, 
set the value to "immunity" and heat map the results. Similarly, for the current infection geopackage, set the value to "Level of Community Transmission" and heat map the results. Of course, 
the mapping can vary greatly in furture iterations of this code depending on which aspects of immnunity and infection are desriable and interesting to display. 
