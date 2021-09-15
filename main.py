import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import requests
from cryptocompy import coin
from cryptocompy import price

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