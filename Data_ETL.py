#importing required packages
import math
import pandas as pd
import requests as req
import json

#getting  variables necessary for API calls

indicators = []
countries = [] #take 20 countries with largest gdp

parameters={'country':'all',
            'id':'SP.POP.TOTL',
            'start_date':'1980',
            'end_date':'2020',
            'page':'1'
                }
population_data = pd.DataFrame()
for page in range(100,102):
    parameters['page']=page
    responded = req.get("https://api.worldbank.org/v2/country/{country}/indicator/{id}?date={start_date}:{end_date}&format=json&page={page}".format_map(parameters))
    #responded = req.get("https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?date=2000:2020&format=json&page={}".format(page))
    #print(type(responded))
    responded=responded.json()[1]
    temp_df = pd.DataFrame(responded)[['country', 'countryiso3code', 'date', 'value', 'unit',
       'obs_status', 'decimal']]
    temp_df.rename(columns={'value':'population'},inplace=True)
    print(population_data.columns)
    temp_df = pd.concat([temp_df, temp_df["country"].apply(pd.Series)], axis=1)
    population_data = pd.concat([temp_df, population_data], ignore_index=True)
    print(page, " pages done")

population_data.drop(columns=['country'],inplace=True)
population_data.rename(columns={'id':'country_code','value':'country_name'},inplace=True)
print(population_data.head(5))
print(population_data.describe())

