# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 21:12:23 2022

@author: Patryk Swiatek
"""

import pandas as pd

ResultMatrix = list()
ResultMatrix.append(['name','datetime','tempmax','tempmin','temp',
            'feelslikemax','feelslikemin','feelslike','dew','humidity','precip',
            'precipprob','precipcover','preciptype','snow',
            'snowdepth','windgust','windspeed','winddir','sealevelpressure','cloudcover',
            'visibility','solarradiation','solarenergy','uvindex','severerisk',
            'sunrise','sunset','moonphase','conditions','description','icon','stations'])

CityName = list()

df_races = pd.read_csv('C:\\Users\\patry\\OneDrive\\Pulpit\\Zdalne pw\\Hurtownie danych i systemy BI\\Projekt\\races.csv')
df_circuits = pd.read_excel('C:\\Users\\patry\\OneDrive\\Pulpit\\Zdalne pw\\Hurtownie danych i systemy BI\\Projekt\\circuitsv2.xlsx')


df_merged = df_races.merge(df_circuits, left_on='circuitId', right_on='circuitId')[['location','date']]
df_merged.columns = ['city_name', 'date']

#Downloading weather data using Python as a CSV using the Visual Crossing Weather API
#See https://www.visualcrossing.com/resources/blog/how-to-load-historical-weather-data-using-python-without-scraping/ for more information.
import csv
import codecs
import urllib.request
import urllib.error
import sys

BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

ApiKey='Z6WGSJRKP6K3WKK3LH6AUWDMX'
UnitGroup='us'

def replace_api(word):
    word_rep = word.replace('Yeongam County','34.7333%2C%20126.417')
    word_rep = word_rep.replace(' ', '%20')
    word_rep = word_rep.replace('ó', '%C3%B3')
    word_rep = word_rep.replace('ü', '%C3%BC')
    word_rep = word_rep.replace('Baku', '40.3725%2C49.8533')
    return word_rep


for i in range(df_merged.shape[0]):
    if df_merged.iloc[i,1] >= '1970-01-01':

        #Location for the weather data
        Location = replace_api(df_merged.iloc[i,0])
        
        #Optional start and end dates
        #If nothing is specified, the forecast is retrieved. 
        #If start date only is specified, a single historical or forecast day will be retrieved
        #If both start and and end date are specified, a date range will be retrieved
        StartDate = df_merged.iloc[i,1]
        EndDate=''
        
        #JSON or CSV 
        #JSON format supports daily, hourly, current conditions, weather alerts and events in a single JSON package
        #CSV format requires an 'include' parameter below to indicate which table section is required
        ContentType="csv"
        
        #include sections
        #values include days,hours,current,alerts
        Include="days"
        
        
        print('')
        print(' - Requesting weather : ')
        
        #basic query including location
        ApiQuery=BaseURL + Location
        
        #append the start and end date if present
        if (len(StartDate)):
            ApiQuery+="/"+StartDate
            if (len(EndDate)):
                ApiQuery+="/"+EndDate
        
        #Url is completed. Now add query parameters (could be passed as GET or POST)
        ApiQuery+="?"
        
        #append each parameter as necessary
        if (len(UnitGroup)):
            ApiQuery+="&unitGroup="+UnitGroup
        
        if (len(ContentType)):
            ApiQuery+="&contentType="+ContentType
        
        if (len(Include)):
            ApiQuery+="&include="+Include
        
        ApiQuery+="&key="+ApiKey
        
        
        
        print(' - Running query URL: ', ApiQuery)
        print()
        
        try: 
            CSVBytes = urllib.request.urlopen(ApiQuery)
        except urllib.error.HTTPError  as e:
            ErrorInfo= e.read().decode() 
            print('Error code: ', e.code, ErrorInfo)
            sys.exit()
        except  urllib.error.URLError as e:
            ErrorInfo= e.read().decode() 
            print('Error code: ', e.code,ErrorInfo)
            sys.exit()
        
        
        # Parse the results as CSV
        CSVText = csv.reader(codecs.iterdecode(CSVBytes, 'utf-8'))
        
        
        RowIndex = 0
        
        # The first row contain the headers and the additional rows each contain the weather metrics for a single day
        # To simply our code, we use the knowledge that column 0 contains the location and column 1 contains the date.  
        #The data starts at column 4

        for Row in CSVText:
            if RowIndex == 0:
                FirstRow = Row
            else:
                ResultMatrix.append(Row)
                CityName.append(df_merged.iloc[i,0])
                print('Weather in ', Row[0], ' on ', Row[1])
        
                ColIndex = 0
                for Col in Row:
                    if ColIndex >= 4:
                        print('   ', FirstRow[ColIndex], ' = ', Row[ColIndex])
                    ColIndex += 1
            RowIndex += 1
        
        # If there are no CSV rows then something fundamental went wrong
        if RowIndex == 0:
            print('Sorry, but it appears that there was an error connecting to the weather server.')
            print('Please check your network connection and try again..')
        
        # If there is only one CSV  row then we likely got an error from the server
        if RowIndex == 1:
            print('Sorry, but it appears that there was an error retrieving the weather data.')
            print('Error: ', FirstRow)

            
            
test = pd.DataFrame(ResultMatrix[1:], columns=ResultMatrix[0])
test['CityName'] = CityName

test.to_csv(path_or_buf='C:\\Users\\patry\\OneDrive\\Pulpit\\Zdalne pw\\Hurtownie danych i systemy BI\\Projekt\\weather_2.txt',
            sep=';')


#dane pogodowe z tego zrodla istnieja jedynie od roku 1970, takie sa generowane 
    
