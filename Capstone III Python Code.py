#Capstone was analyzing any relationship between a planet's total orbit duration and
#its mass or its host star's mass.
#view the full Google Colab Python Notebook here: 
#https://colab.research.google.com/drive/1UldmqYGivkGUBs8p3zgk8Q-ox8Qxo2im?usp=sharing



#module imports

import requests
import io

import math
import statistics

from scipy import stats
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Table Access Protocol API to retrieve exoplanet data from the Nasa Exoplanet Archive
# API documentation: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html

api_base_url = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query='
api_query_url = 'select+pl_name,pl_orbper,pl_masse,hostname,st_mass+from+ps'
api_format_url = '&format=csv'
api_output = requests.get(api_base_url + api_query_url + api_format_url).content


#convert contents of API Output into a CSV-format which then can be read into a DataFrame using the pd.read_csv method, DataFrame named as "CosmicTable"
CosmicTable = pd.read_csv(io.StringIO(api_output.decode('utf-8')))


#remove rows which have a missing value under any column for the newly created DataFrame
CosmicTable = CosmicTable.dropna(axis=0)


#Create DataFrames for Pearson Correlation Test and T-Test
PlanetsHostGreater1 = CosmicTable.loc[CosmicTable['st_mass'] >= 1 ]
PlanetsHostLesser1 = CosmicTable.loc[CosmicTable['st_mass'] < 1 ]

PlanetsMass = CosmicTable.drop(['hostname', 'st_mass'], axis=1)


#Pearson Correlation Test between planets' mass and their total orbit duration 
#Various code included which was used for viewing descriptive stats
PlanetsMass.describe()
statistics.median(PlanetsMass['pl_orbper'])
pearsonresults = stats.pearsonr(PlanetsMass['pl_orbper'], PlanetsMass['pl_masse'])
sns.scatterplot(data=PlanetsMass, x='pl_masse', y='pl_orbper') 


#Independent T-Test between planets' orbit duration for with heavier host stars vs not-as-heavy host stars.
#Various code included which was used to view descriptive stats
PlanetsHostGreater1['pl_orbper'].describe()
sns.scatterplot(x='st_mass', y='pl_orbper', data=PlanetsHostGreater1)
statistics.median(PlanetsHostGreater1['pl_orbper'])
PlanetsHostLesser1['pl_orbper'].describe()
sns.scatterplot(x='st_mass', y='pl_orbper', data=PlanetsHostLesser1)
statistics.median(PlanetsHostLesser1['pl_orbper'])
ttestresults = stats.ttest_ind(PlanetsHostGreater1['pl_orbper'], PlanetsHostLesser1['pl_orbper'])


#results
print(f"Pearson results were {pearsonresults}, displaying Pearson coefficient and P-value respectively. And t-test results were {ttestresults}, displaying T-stat and P-value respectively. Failed to reject Pearson null hypothesis on the basis of a 95% confidence interval due to the Pearson coefficient being close to 0, indicating evidence towards no positive relationship, and the P-value being greater than 0.05, showing evidence for higher probability that we'd excavate data as extreme as this. Failed to reject T-test null hypothesis on the basis of a 95% confidence interval due to the T-value being less than 1.96 and the p-value being greater than 0.05.")


#view the full Google Colab Python Notebook here: 
#https://colab.research.google.com/drive/1UldmqYGivkGUBs8p3zgk8Q-ox8Qxo2im?usp=sharing