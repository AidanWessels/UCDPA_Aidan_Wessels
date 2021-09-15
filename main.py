import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import requests
from cryptocompy import coin

#2  Importing Data

#2a Retreive Data fom online APIs
#Example 1
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
bitcoin_data = response.json()
print(bitcoin_data)

#Example 2
api_request = requests.get('http://api.open-notify.org/astros.json')

my_api_data = api_request.text
mydatajson = api_request.json()

print(my_api_data)
print(mydatajson)
print(mydatajson["number"])

#Example 3
start_date = dt.datetime(2019,11,2)
end_date = dt.datetime(2020,9,11)

stock_data = web.DataReader("NFLX", 'yahoo', start_date, end_date)
print(stock_data)

#Example 4 - This will be used later when analysing lists and dictionaries
coin_data = coin.get_coin_list()
symbols = list(coin_data.keys())
print(symbols)

#2b Import a CSV file into a Pandas DataFrame
crypto_data = pd.read_csv('all_currencies.csv')

print(crypto_data.shape)
print(crypto_data.info)

print(crypto_data)


data = pd.read_csv('all_currencies.csv')
data2 = pd.read_csv('crypto_prices.csv')

#3 Analysing Data
#3a.1. Sort
data_date_sort = data.sort_values(by=['Date'], axis=0, na_position='last')
data_high_sort = data.sort_values(by=['High'], axis=0, ascending = 0, na_position='last')

print(data_date_sort)
print(data_high_sort[['Date','High','Symbol']])

#3a.2 Index
indexed_data = data.index[data['Symbol'] == 'NANOX']

#print(data[indexed_data])

#3a.3 Group
grouped_data = data[(data.Symbol != '$$$')]
data_highest_per_currency = data[data.groupby('Symbol').High.transform('max') == data['High']]

print(grouped_data)
print(data_highest_per_currency[['Date','Symbol','High']])

#3b Replacing missing values

data[['Market Cap']] = data[['Market Cap']].fillna(method="bfill",axis=0).fillna(method="ffill",axis=0)

print(data)

#3c Looping, iterrows

#NOTE - Running this is very computationally heavy
for label, row in data.iterrows():
    data.loc[label,'Circulating Supply'] = row['Market Cap']/row['Close']
print(data)

#3d Merge DataFrames

data2.rename(columns={"DateTime": "Date"}, inplace=True)
data['Date'] = pd.to_datetime(data['Date'])
data2['Date']= pd.to_datetime(data2['Date'])
data2['Date'] = pd.to_datetime(data2["Date"].dt.strftime('%Y-%m-%d'))

ETH_data = data[(data['Symbol']=='ETH')]
ETH_data2 = data2[(data2['Symbol']=='ETH')]


ETH_merged_data = ETH_data.merge(ETH_data2, how='inner', left_on=["Symbol","Date"], right_on=["Symbol","Date"])
print(ETH_merged_data.head())


#4a_Define a custom function to create reuseable code

grouped_data = data[(data.Symbol == '$$$')]

def fill_missiing_data(data, fillvalue=0):
    data = data.copy()
    for i, value in enumerate(data['Market Cap'].values):
        if np.isnan(value):
            data['Market Cap'][i] = fillvalue
    return(data)

print(fill_missiing_data(grouped_data))

#4b Numpy

print(np.sort(data.Symbol.unique()))

#4c Dictionary or Lists

coin_data = coin.get_coin_list()
symbols = list(coin_data.keys())

coin_list = coin.get_coin_list(coins=["BTC", "ETH"])

print(coin_list)
print(symbols[:1])

print(coin_data['BTCD'])

company = coin_data.get('MTCE', 'MISSING')
print(company)