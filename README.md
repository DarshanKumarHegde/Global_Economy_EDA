# **Economy Indicators EDA**

>EDA Project to understand key Global Economy Indicators, their relationships and impacts on a country's economy in general.
---
## *Key Indicators extracted from the Database*
|	Code |	License Type |	Indicator Name |
|	:--: | :-----------: |	:------------: |
|EG.USE.ELEC.KH.PC	|Use and distribution of these data are subject to IEA terms and conditions.|	Electric power consumption (kWh per capita)|
|EG.USE.PCAP.KG.OE	|Use and distribution of these data are subject to IEA terms and conditions.|	Energy use (kg of oil equivalent per capita)|
|NE.EXP.GNFS.ZS	|CC BY-4.0|	Exports of goods and services (% of GDP)|
|DT.DOD.DECT.CD	|CC BY-4.0|	External debt stocks, total (DOD, current US$)|
|BX.KLT.DINV.CD.WD	|CC BY-4.0|	Foreign direct investment, net inflows (BoP, current US$)|
|NY.GDP.MKTP.CD |CC BY-4.0|	GDP (current US$)|
|NY.GDP.MKTP.KD.ZG	|CC BY-4.0|	GDP growth (annual %)|
|NE.IMP.GNFS.ZS |CC BY-4.0|	Imports of goods and services (% of GDP)|
|SI.DST.FRST.20	|CC BY-4.0|	Income share held by lowest 20%|
|NY.GDP.DEFL.KD.ZG	|CC BY-4.0|	Inflation, GDP deflator (annual %)|
|SP.DYN.LE00.IN	|CC BY-4.0|	Life expectancy at birth, total (years)|
|EN.POP.DNST	|CC BY-4.0|	Population density (people per sq. km of land area)|
|SP.POP.GROW	|CC BY-4.0|	Population growth (annual %)|
|SP.POP.TOTL	|CC BY-4.0|	Population, total|
|SI.POV.NAHC	|CC BY-4.0|	Poverty headcount ratio at national poverty lines (% of population)|
|GC.REV.XGRT.GD.ZS	|CC BY-4.0|	Revenue, excluding grants (% of GDP)|
|AG.SRF.TOTL.K2	|CC BY-4.0|	Surface area (sq. km)|
|GC.TAX.TOTL.GD.ZS	|CC BY-4.0|	Tax revenue (% of GDP)|
|DT.TDS.DECT.EX.ZS	|CC BY-4.0|	Total debt service (% of exports of goods, services and primary income)|
|SP.URB.GROW	|CC BY-4.0|	Urban population growth (annual %)|
--- 
<br/>*There are numerous other indicators on the WorldBank Database, but I have chosen only those that are probably useful for my current study*

## Categorizing the above Indicators to use in my study
1. Country descriptors
    - Surface area (sq. km) : AG.SRF.TOTL.K2
    - GDP (current US$) : NY.GDP.MKTP.CD
    - GDP growth (annual %) : NY.GDP.MKTP.KD.ZG
    - Urban Population growth (annual %) : SP.POP.GROW
    - Population, total : SP.POP.TOTL
    - Population density (people per sq. km of land area) : EN.POP.DNST

3. Trade 
    - Foreign direct investment, net inflows (BoP, current US$) : BX.KLT.DINV.CD.WD
    - Imports of goods and services (% of GDP) : NE.IMP.GNFS.ZS
    - Exports of goods and services (% of GDP) : NE.EXP.GNFS.ZS

4. Other indicators
    - Inflation, GDP deflator (annual %) : NY.GDP.DEFL.KD.ZG
    
<br/>*Above 4 categories are used for the study. You may find few indicators that were collected are ignored, just so that there are fewer but relevent indicators*

## *Data Source and other required links*
- Database - [DataBank | The World Bank](https://data.worldbank.org/) 
- API documentation - [World Bank | Developer information](https://datahelpdesk.worldbank.org/knowledgebase/topics/125589)
