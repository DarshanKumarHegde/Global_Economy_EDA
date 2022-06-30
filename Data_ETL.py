#importing required packages
import math
import pandas as pd
import requests as req
import json
import numpy as np

def ETL():
    #getting required countries from the  countries API of worldbank as a table
    countriesAPI = 'https://api.worldbank.org/v2/country?format=json&per_page=300'
    response = req.get(countriesAPI)
    print(response.status_code)
    countryDF = pd.DataFrame(response.json()[1])[['id','name', 'capitalCity']]
    countryDF.replace('',np.nan, inplace=True)

    #extracting groups and aggregates of countries like - EU, UAE and others as in WorldBank dataset
    aggregateDF=countryDF[countryDF['capitalCity'].isnull()]
    aggregateDF.to_csv('CountryGroupsAndAggregates.csv', index=False)

    #extracting individual countries
    countryDF.dropna().reset_index(drop=True).loc[:,['id','name']]
    countryDF.to_csv('Countries.csv',index=False)

    #getting  variables necessary for API calls
    #indicators are variables for worldbank dataset
    indicators = pd.read_excel('Data_Extract_From_World_Development_Indicators_Metadata.xlsx', 
                                sheet_name='Series - Metadata')[['Required','Code','Indicator Name']]
    indicators.dropna(inplace=True)
    indicators.drop(columns=['Required'])
    indicatorList = indicators['Code'].tolist()
    print('indicators are', indicatorList)

    #parameters contain necessary strings to include in API call
    parameters={'country':'all',
                'id':'IDOfTheIndicator',
                'startDate':'1990',
                'endDate':'2020',
                'pages':1
                    }

    #'data' is a temporary dataframe to store data for each indicator looped, finalData is the merge of all indicators
    data = pd.DataFrame()
    finalData = pd.DataFrame()

    #for each Indicator, get data from the API
    try:
        for indicator_idx, indicator in enumerate(indicatorList):

            #setting the parameter dictionary for the current indicator
            parameters['id']=indicator
            print('fetching data for', indicator)
            getTotalPages = req.get("https://api.worldbank.org/v2/country/{country}/indicator/{id}?date={startDate}:{endDate}&format=json".format_map(parameters))
            #get the total number of pages for the current API call  
            totalPages=getTotalPages.json()[0]['pages']
            print(totalPages)

            for page in range(1,totalPages):
                parameters['pages'] = page
                getDataForIndicator = req.get("https://api.worldbank.org/v2/country/{country}/indicator/{id}?date={startDate}:{endDate}&format=json&page={pages}".format_map(parameters))
                #print(getDataForIndicator.status_code)
                try:
                    getDataForIndicator=getDataForIndicator.json()[1]
                    temp_data = pd.DataFrame(getDataForIndicator)[['country', 'countryiso3code', 'date', 'value','unit','obs_status','decimal']]
                    
                except:
                    indicatorList=indicatorList[indicator_idx+1:]
                    temp_data = pd.DataFrame()
                    data = pd.DataFrame()
                    print('pipe broke while at page',page)
                    break
                else:
                    data=pd.concat([data, temp_data])
                    if page%5==0: print(page,' pages done')
                    
            try:    #indName = indicators.loc[indicator,'Indicator Name']
                data.rename(columns={'value':indicator},inplace=True)
                data = pd.concat([data, data['country'].apply(pd.Series)], axis=1)
                data.drop(columns=['country'], inplace=True)
                data.rename(columns={'id':'country code','value':'country'}, inplace=True)
            except:
                indicatorList=indicatorList[indicator_idx:]
                temp_data = pd.DataFrame()
                data = pd.DataFrame()
                print('pipe broke while at page',page)
                continue


        #merging data into finalData dataframe, so it contains rows of country names and indicators in columns
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
    except:
        print('pipe broke at indicator ',indicator, ' while at page-',page)
    finally:
        print(finalData.head(50))
        print(finalData.columns, finalData.shape, finalData.describe())
        
        #exception handling for writing data into csv
        try:
            finalData.to_csv('IndicatorsData.csv')
            print('indicator -', indicator)
            print('data written succesfully')
        except:
            print('data write unsuccesful')


