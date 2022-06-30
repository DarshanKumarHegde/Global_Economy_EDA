import pandas as pd
import numpy as np
import requests as req
import json
import math
import os

#dictionary to pass parameters for APIurl
parameters = {'country':'all','id':'IDOfTheIndicator',
            'startDate':'1990','endDate':'2020',
            'pages':1
                }

def get_indicators():
    #get required indicators marked in the Metadata file 
    indicators = pd.read_excel('Data_Extract_From_World_Development_Indicators_Metadata.xlsx', 
                            sheet_name='Series - Metadata')[['Required','Code','Indicator Name']]
    indicators.dropna(inplace=True)
    indicators.drop(columns=['Required'])
    indicatorList = indicators['Code'].tolist()
    print('indicators are', indicatorList)
    return indicatorList

def get_totalPages(indicator, parameters=parameters):
    #function to get the total number of pages the API has for the given indicator
    parameters['id']=indicator
    print('indicator set to -', indicator)
    getTotalPages = req.get("https://api.worldbank.org/v2/country/{country}/indicator/{id}?date={startDate}:{endDate}&format=json".format_map(parameters))
    return getTotalPages.json()[0]['pages']

def extract_data(parameters, indicator):
    APIurl = "https://api.worldbank.org/v2/country/{country}/indicator/{id}?date={startDate}:{endDate}&format=json".format_map(parameters)
    data = pd.DataFrame()
    #setting the indicator in the parameter dictionary
    parameters['id']= indicator

    #following two variables are to keep track of repetitions of same page if caught under except
    repetition_count, repeated_page = 1, -1
    print('fetching data for', indicator)
    totalPages = get_totalPages(indicator, parameters)

    #going through each page for the indicator
    for page in range(1,totalPages+1):
        parameters['pages']=page
        getDataForIndicator = req.get("https://api.worldbank.org/v2/country/{country}/indicator/{id}?date={startDate}:{endDate}&format=json&page={pages}".format_map(parameters))
        try:
            DataForIndicator=getDataForIndicator.json()[1]
            temp_data = pd.DataFrame(DataForIndicator)[['country', 'countryiso3code', 'date', 'value']]   
        except:
            if page==repeated_page: 
                repetition_count+=1
            if repetition_count==3:
                print('pipe broke at page', page, 'repetitions done')
                break
            repeated_page=page
            page-=1
            temp_data = pd.DataFrame()
            print('pipe broke while at page',page, 'redoing the page')
            continue
        else:
            data=pd.concat([data, temp_data])
            if page%5==0: print(page,' pages done')
            repetition_count=1
            temp_data=pd.DataFrame()

    #data.drop(columns=['unit','obs_status','decimal'],inplace=True)
    data.rename(columns={'value':indicator},inplace=True)
    data = pd.concat([data, data['country'].apply(pd.Series)], axis=1)
    data.drop(columns=['country'], inplace=True)
    data.rename(columns={'id':'country code','value':'country'}, inplace=True)

    data.replace('',np.nan, inplace=True)

    folder, filename = 'dataset', indicator+'data.csv'
    data.to_csv(os.path.join(folder,filename), index=False)


indicatorList = get_indicators()

extract_data(parameters,indicatorList[0])


#for indicator in indicatorList:
#    extract_data(parameters, indicator)