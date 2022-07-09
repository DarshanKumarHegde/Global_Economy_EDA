import math
from operator import concat
from re import split
import numpy as np
import pandas as pd

#getting indicators description to replace indicator IDs in the data
indicators = pd.read_excel('Data_Extract_From_World_Development_Indicators_Metadata.xlsx', usecols=['Code', 'Indicator Name'])

#read the csv data file
data_df = pd.read_csv('IndicatorsData.csv')

data_df.fillna(0)
data_df.replace(np.nan, 0)
print(data_df.value_counts())