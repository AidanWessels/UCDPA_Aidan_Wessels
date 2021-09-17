import numpy as np
import pandas as pd
from datetime import datetime as dt, timedelta
import pandas_datareader.data as web
import requests
from cryptocompy import coin
from cryptocompy import price
import matplotlib.pyplot as plt

#2  Importing Data

#2a Retreive Data fom online APIs
#Example 1 Get up to date Bitcoin data
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
bitcoin_data = response.json()
#Print the results
print(bitcoin_data

#Example 2 Retrieve up Stock data over a period - uses DataReader
start_date = dt.datetime(2019,11,2)
end_date = dt.datetime(2020,9,11)

stock_data = web.DataReader("NFLX", 'yahoo', start_date, end_date)
#Print the results
print(stock_data)

#Example 3 - This will be used later when analysing lists and dictionaries
coin_data = coin.get_coin_list()
symbols = list(coin_data.keys())
#Print the results
print(symbols)

#2b Import a CSV file into a Pandas DataFrame
data = pd.read_csv('all_currencies.csv')
data2 = pd.read_csv('crypto_prices.csv')

#Print data relating to our dataset 'all_currencies.csv'
print(data.shape)
print(data.info)
print(data)

#Print data relating to our dataset 'crypto_prices.csv'
print(data2.shape)
print(data2.info)
print(data2)

#3 Analysing Data
#3a.1. Sort - Data sorted by Date and High prices
data_date_sort = data.sort_values(by=['Date'], axis=0, na_position='last')
data_high_sort = data.sort_values(by=['High'], axis=0, ascending = 0, na_position='last')

#Print the results
print(data_date_sort)
print(data_high_sort[['Date','High','Symbol']])

#3a.2 Index - Using index return only records where the Symbol == 'NANOX'
indexed_data = data.index[data['Symbol'] == 'NANOX']

#Print the results
print(data[indexed_data])

#3a.3 Group - Group data where the Symbol is NOT equal to '$$$' and where the Symbol is BTC ONLY.
grouped_data = data[(data.Symbol != '$$$')]
grouped_BTC_data = data[(data.Symbol == 'BTC')]

#Print the results
print(grouped_data)
print(grouped_BTC_data)

#3a.3 Group - Group data by Symbol for the max High price attained.
data_highest_per_currency = data[data.groupby('Symbol').High.transform('max') == data['High']]

#Print the results
print(data_highest_per_currency[['Date','Symbol','High']])

#3b Replacing missing values - using teh fillna bfill and ffill functions
data[['Market Cap']] = data[['Market Cap']].fillna(method="bfill",axis=0).fillna(method="ffill",axis=0)
#This is done for the Bitcoin only data aswell, which will be used in 3c to calcualte 'Circulating Supply'
grouped_BTC_data[['Market Cap']] = grouped_BTC_data[['Market Cap']].fillna(method="bfill",axis=0).fillna(method="ffill",axis=0)

#Print the results
print(data)
print(grouped_BTC_data)

#3c Looping, iterrows - use a for loop to calculate the 'Circulating Supply' for each row of Bitcoin data
#NOTE - Running this is very computationally heavy
for label, row in grouped_BTC_data.iterrows():
    grouped_BTC_data.loc[label,'Circulating Supply'] = row['Market Cap']/row['Close']
#Print the results
print(grouped_BTC_data)

#3d Merge DataFrames
#Rename the Date column in the dataset to match that of dataset 1
data2.rename(columns={"DateTime": "Date"}, inplace=True)
#Convert the datatypes so that they match for both the datasets
data['Date'] = pd.to_datetime(data['Date'])
data2['Date']= pd.to_datetime(data2['Date'])
data2['Date'] = pd.to_datetime(data2["Date"].dt.strftime('%Y-%m-%d'))

#Extract only the records where the Symbol is ETH for both datasets
ETH_data = data[(data['Symbol']=='ETH')]
ETH_data2 = data2[(data2['Symbol']=='ETH')]

#Merge the datasets
ETH_merged_data = ETH_data.merge(ETH_data2, how='inner', left_on=["Symbol","Date"], right_on=["Symbol","Date"])
#Print the results
print(ETH_merged_data.head())

#4a_Define a custom function to create reuseable code
#Extract only the records where the Symbol = '$$$'
grouped_data = data[(data.Symbol == '$$$')]

def fill_missiing_data(data, fillvalue=0):
    data = data.copy()
    for i, value in enumerate(data['Market Cap'].values):
        if np.isnan(value):
            data['Market Cap'][i] = fillvalue
    return(data)

#Print the results
print(fill_missiing_data(grouped_data))

#4b Numpy
#Print a list of the unique Symbols in the dataset
print(np.sort(data.Symbol.unique()))

#4c Dictionary or Lists

coin_data = coin.get_coin_list()
cryto_symbols = list(coin_data.keys())

#Print the complete list of Cryptocurrency symbols
print(cryto_symbols)
#Pring only the first 5 symbols in the coin_data symbols list
print(cryto_symbols[:5])

#Get coin data for AMC and CRYPT
coin_data_amc_crypt = coin.get_coin_list(coins=["AMC", "CRYPT"])
print(coin_data_amc_crypt)

#Get coin data for LTCX
print(coin_data['LTCX'])

#Find coin data for coin = MTCE where no data available print 'MISSING'
company = coin_data.get('MTCE', 'MISSING')
print(company)

#Get Bitcoins latest prices relative to EUR, USD, BTCD and BTCE
bitcoin_prices = price.get_current_price("BTC", ["EUR", "USD", "BTCD", "BTCE"])
print(bitcoin_prices)

#5 Visualise
#Ensure 'Date' column is converted to datatype 'datetime'
data['Date'] = pd.to_datetime(data['Date'])
dope_data = data[(data.Symbol == 'DOPE')]
btc_data = data[(data.Symbol == 'BTC')]

#Find the start date of the dataset where currency symbol = DOPE
start_date = dope_data['Date'].min()
#Find the end date of the dataset where currency symbol = DOPE
end_date = dope_data['Date'].max()
#Find the start date of the last year of the dataset where currency symbol = DOPE
last_year = end_date - timedelta(days=365)

full_data_mask = (dope_data['Date'] > start_date) & (dope_data['Date'] <= end_date)
full_dope_data = dope_data.loc[full_data_mask]

last_year_data_mask = (dope_data['Date'] > last_year) & (dope_data['Date'] <= end_date)
last_year_dope_data = dope_data.loc[last_year_data_mask]

last_year_data_mask = (btc_data['Date'] > last_year) & (btc_data['Date'] <= end_date)
last_year_btc_data = btc_data.loc[last_year_data_mask]

#Create Figure 1
plt.figure(1)
plt.plot(full_dope_data['Date'],full_dope_data['Close'], color = 'red')
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('DOPE Data over the Entire Dataset')

#Create Figure 2
plt.figure(2)
plt.plot(last_year_dope_data['Date'],last_year_dope_data['Close'], color = 'green')
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('DOPE Data over the most recent year only')

#Create Figure 3
plt.figure(3)
plt.plot(last_year_btc_data['Date'],last_year_btc_data['Close'], color = 'orange')
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('BTC Data over the most recent year only')

plt.show()