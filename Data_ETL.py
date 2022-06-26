#importing required packages
import math
import pandas as pd
import requests as req

#getting variables necessary for API calls
responded = req.get("https://api.worldbank.org/v2/en/sources/15/series/all/metadata?page=1&per_page=20000&format=json")
data = responded.json()["source"][0]["concept"][0]['variable']
df = pd.DataFrame(data)[["id"]]

id_list=df.to_dict()
print(id_list)