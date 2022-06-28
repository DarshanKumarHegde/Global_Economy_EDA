#importing required packages
import math
import pandas as pd
import requests as req
import json
import numpy as np

#getting required countries from the  countries API of worldbank as a table
countriesAPI = 'https://api.worldbank.org/v2/country?format=json&per_page=300'
response = req.get(countriesAPI)
print(response.status_code)
countryDF = pd.DataFrame(response.json()[1])[['id','name', 'capitalCity']]
countryDF.replace('',np.nan, inplace=True)
countryDF.dropna().reset_index(drop=True).loc[:,['id','name']]

#getting  variables necessary for API calls
#countryIDs= ';'.join(countryDF['id']).lower() #country id formatted for the API
indicators = pd.read_excel('Data_Extract_From_World_Development_Indicators_Metadata.xlsx', 
                            sheet_name='Series - Metadata')[['Required','Code','Indicator Name']]
indicators.dropna().drop(columns=['Required'])
indicatorList = indicators['Code'].tolist()
print('indicators are', indicatorList)


parameters={'country':'all',
            'id':'IDOfTheIndicator',
            'startDate':'1990',
            'endDate':'2020',
            'pages':1
                }

data = pd.DataFrame()
finalData = pd.DataFrame()
#for each Indicator, get data from the API
for indicator in indicatorList:
    #setting the parameter dictionary for the current indicator
    parameters['id']=indicator
    print('fetching data for', indicator)
    getTotalPages = req.get("https://api.worldbank.org/v2/country/{country}/indicator/{id}?date={startDate}:{endDate}&format=json".format_map(parameters))
    #print(getTotalPages.status_code)
    #get the total number of pages for the current API call  
    totalPages=getTotalPages.json()[0]['pages']

    for page in range(1,totalPages):
        parameters['pages'] = page
        getDataForIndicator = req.get("https://api.worldbank.org/v2/country/{country}/indicator/{id}?date={startDate}:{endDate}&format=json&page={pages}".format_map(parameters))
        #print(getDataForIndicator.status_code)
        getDataForIndicator=getDataForIndicator.json()[1]
        temp_data = pd.DataFrame(getDataForIndicator)[['country', 'countryiso3code', 'date', 'value', 'unit',
        'obs_status', 'decimal']]
        data=pd.concat([data, temp_data])
        print(page,' pages done')

        #indName = indicators.loc[indicator,'Indicator Name']
    data.rename(columns={'value':indicator},inplace=True)
    data = pd.concat([data, data["country"].apply(pd.Series)], axis=1)
    data.drop(columns=['country'], inplace=True)
    data.rename(columns={'id':'country code','value':'country'}, inplace=True)
    
    if finalData.empty:
        finalData = data
        finalData.drop(columns=['unit','obs_status','decimal'],inplace=True)
        print('Dataframe was empty')
        data=pd.DataFrame()
    else:
        finalData = pd.merge(finalData,
                        data[['countryiso3code','country code','country', 'date',indicator]],
                        how='left', 
                        on=['countryiso3code','country code','country','date',])
        data=pd.DataFrame()
print(finalData.head(50))
print(finalData.columns, finalData.shape, finalData.describe())

try:
    finalData.to_csv('IndicatorsData.csv')
    print('data written succesfully')
except:
    print('data write unsuccesful')