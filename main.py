import numpy as np
import pandas as pd
import datetime as dt
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
print(bitcoin_data)

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
print(indexed_data)

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
data[['Market Cap']] = data[['Market Cap']].fillna(method="bfill",axis=0)
#This is done for the Bitcoin only data aswell, which will be used in 3c to calcualte 'Circulating Supply'
grouped_BTC_data[['Market Cap']] = grouped_BTC_data[['Market Cap']].fillna(method="bfill",axis=0)

#Print the results
print(data)
print(grouped_BTC_data)

#3c Looping, iterrows - use a for loop to calculate the 'Circulating Supply' for each row of Bitcoin data
#NOTE - Running this is will give warnings
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
#Extract only the records where the Symbol = 'DOGE'
grouped_doge_data = data[(data.Symbol == 'DOGE')]

def fill_missiing_data(data, fillvalue=0):
    data = data.copy()
    for i, value in enumerate(data['Market Cap'].values):
        if np.isnan(value):
            data['Market Cap'][i] = fillvalue
    return(data)

#Print the results
print(fill_missiing_data(grouped_doge_data))

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
from datetime import datetime as dt, timedelta
#Reimport the original DataFrame
data = pd.read_csv('all_currencies.csv')

#Ensure 'Date' column is converted to datatype 'datetime'
data['Date'] = pd.to_datetime(data['Date'])
LTC_data = data[(data.Symbol == 'LTC')]
BCH_data = data[(data.Symbol == 'BCH')]

#Find the start date of the dataset where currency symbol = DOPE
start_date = LTC_data['Date'].min()
#Find the end date of the dataset where currency symbol = DOPE
end_date = LTC_data['Date'].max()
#Find the start date of the last year of the dataset where currency symbol = DOPE
last_year = end_date - timedelta(days=365)

full_LTC_data = LTC_data.loc[(LTC_data['Date'] > start_date) & (LTC_data['Date'] <= end_date)]
full_BCH_data = BCH_data.loc[(BCH_data['Date'] > start_date) & (BCH_data['Date'] <= end_date)]

last_year_LTC_data = LTC_data.loc[(LTC_data['Date'] > last_year) & (LTC_data['Date'] <= end_date)]
last_year_BCH_data = BCH_data.loc[(BCH_data['Date'] > last_year) & (BCH_data['Date'] <= end_date)]

#Create Figure 1
plt.figure(1)
plt.plot(full_LTC_data['Date'],full_LTC_data['Close'], color = 'red', label="Litecoin")
plt.plot(full_BCH_data['Date'],full_BCH_data['Close'], color = 'green', label="Bitcoin Cash")
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('LTC & BCH Data over the Entire Dataset')
plt.legend()
plt.xticks(rotation = 45)

#Create Figure 2
plt.figure(2)
plt.plot(last_year_LTC_data['Date'],last_year_LTC_data['Close'], color = 'red', label="Litecoin")
plt.plot(last_year_BCH_data['Date'],last_year_BCH_data['Close'], color = 'green', label="Bitcoin Cash")
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('LTC & BCH Data over over the most recent year only')
plt.legend()
plt.xticks(rotation = 45)

#Create Figure 3
plt.figure(3)
plt.plot(last_year_LTC_data['Date'],last_year_LTC_data['Close'], color = 'red', label="Litecoin")
plt.plot(last_year_BCH_data['Date'],last_year_BCH_data['Close'], color = 'green', label="Bitcoin Cash")
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('LTC & BCH Data over over the most recent year only - Logarithmic Scale')
plt.legend()
plt.yscale('log')
plt.xticks(rotation = 45)


#With the dataset available we have only a records up to 2018-09-27, this would not include valuable data regarding the COVID-19 pandemic.
#Therefore it would be of further interest to bring in the prices for LTC and BCH since the begining of 2019.
today = dt.now()
start = dt(2019,1,2)
#Determine the number of days since 2019-01-01 to use in the get_historical_data call
delta = today - start

latest_LTC_data = price.get_historical_data('LTC', 'USD', 'day', info='close', aggregate=1, limit=delta.days)
latest_BCH_data = price.get_historical_data('BCH', 'USD', 'day', info='close', aggregate=1, limit=delta.days)

#Get historical prices for LTC
latest_LTC_prices = pd.DataFrame(latest_LTC_data,columns=['time', 'close'])
latest_LTC_prices['time'] = pd.to_datetime(latest_LTC_prices['time'])

#Get historical prices for BCH
latest_BCH_prices = pd.DataFrame(latest_BCH_data,columns=['time', 'close'])
latest_BCH_prices['time'] = pd.to_datetime(latest_BCH_prices['time'])



#Create Figure 4
plt.figure(4)
plt.plot(latest_LTC_prices['time'],latest_LTC_prices['close'], color = 'red', label="Litecoin")
plt.plot(latest_BCH_prices['time'],latest_BCH_prices['close'], color = 'green', label="Bitcoin Cash")
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('LTC & BCH Data since 2019')
plt.legend()
plt.xticks(rotation = 45)


#It would also be useful to do a comparison between Bitcoin and a traditional 'strong' stock
#Get historical prices for Microsoft using DataReader
ms_data = web.DataReader('MSFT', 'yahoo', start, today)
aapl_data = web.DataReader('AAPL', 'yahoo', start, today)


#The Data column is the Key of the dataframe and not a column. In order to use this in Matplotlib we create a new dates column of the same length
dates =[]
for x in range(len(ms_data)):
    newdate = str(ms_data.index[x])
    newdate = newdate[0:10]
    dates.append(newdate)

ms_data['dates'] = dates
#Convert the new 'dates' column to type 'datetime'
ms_data['dates'] = pd.to_datetime(ms_data['dates'])

dates =[]
for x in range(len(aapl_data)):
    newdate = str(aapl_data.index[x])
    newdate = newdate[0:10]
    dates.append(newdate)

aapl_data['dates'] = dates
#Convert the new 'dates' column to type 'datetime'
aapl_data['dates'] = pd.to_datetime(aapl_data['dates'])

#Create Figure 5
plt.figure(5)
plt.plot(ms_data['dates'],ms_data['Close'], color = 'yellow', markevery=100, label="Microsoft")
plt.plot(aapl_data['dates'],aapl_data['Close'], color = 'blue', markevery=100, label="Apple")
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Microsoft and Apple Closing prices since 2019')
plt.legend()
plt.xticks(rotation = 45)

#Combine the datasets for stocks and Crytocurrencies
#Create Figure 7
plt.figure(6)
plt.plot(ms_data['dates'],ms_data['Close'], color = 'yellow', markevery=100, label="Microsoft")
plt.plot(aapl_data['dates'],aapl_data['Close'], color = 'blue', markevery=100, label="Apple")
plt.plot(latest_LTC_prices['time'],latest_LTC_prices['close'], color = 'red', markevery=100, label="LiteCoin")
plt.plot(latest_BCH_prices['time'],latest_BCH_prices['close'], color = 'green', markevery=100, label="Bitcoin Cash")
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Stock Prices vs Cryptocurrency Prices')
plt.xticks(rotation = 45)
plt.legend()

#Create Figure 7
plt.figure(7)
plt.plot(ms_data['dates'],ms_data['Close'], color = 'yellow', markevery=100, label="Microsoft")
plt.plot(aapl_data['dates'],aapl_data['Close'], color = 'blue', markevery=100, label="Apple")
plt.plot(latest_LTC_prices['time'],latest_LTC_prices['close'], color = 'red', markevery=100, label="LiteCoin")
plt.plot(latest_BCH_prices['time'],latest_BCH_prices['close'], color = 'green', markevery=100, label="Bitcoin Cash")
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Stock Prices vs Cryptocurrency Prices - Logarithmic Scale')
plt.xticks(rotation = 45)
plt.yscale('log')
plt.legend()


today = dt.now()
start = dt(2019,1,2)
#Determine the number of days since 2019-01-01 to use in the get_historical_data call
delta = today - start

latest_ETH_data = price.get_historical_data('ETH', 'USD', 'day', info='close', aggregate=1, limit=delta.days)
latest_BTC_data = price.get_historical_data('BTC', 'USD', 'day', info='close', aggregate=1, limit=delta.days)
latest_ADA_data = price.get_historical_data('ADA', 'USD', 'day', info='close', aggregate=1, limit=delta.days)
latest_UNI_data = price.get_historical_data('UNI', 'USD', 'day', info='close', aggregate=1, limit=delta.days)
latest_DOGE_data = price.get_historical_data('DOGE', 'USD', 'day', info='close', aggregate=1, limit=delta.days)

#Get historical prices for ETH
latest_ETH_prices = pd.DataFrame(latest_ETH_data,columns=['time', 'close'])
latest_ETH_prices['time'] = pd.to_datetime(latest_ETH_prices['time'])
#Get historical prices for BTC
latest_BTC_prices = pd.DataFrame(latest_BTC_data,columns=['time', 'close'])
latest_BTC_prices['time'] = pd.to_datetime(latest_BTC_prices['time'])
#Get historical prices for ADA
latest_ADA_prices = pd.DataFrame(latest_ADA_data,columns=['time', 'close'])
latest_ADA_prices['time'] = pd.to_datetime(latest_ADA_prices['time'])
#Get historical prices for UNI
latest_UNI_prices = pd.DataFrame(latest_UNI_data,columns=['time', 'close'])
latest_UNI_prices['time'] = pd.to_datetime(latest_UNI_prices['time'])
#Get historical prices for DOGE
latest_DOGE_prices = pd.DataFrame(latest_DOGE_data,columns=['time', 'close'])
latest_DOGE_prices['time'] = pd.to_datetime(latest_DOGE_prices['time'])

#NOTE this is not the best way to do this. This method was only employed due to time constraints and simplicity - it is computationaly heavy and messy coding.
#NOTE - Running this is will give warnings
merged_data = latest_ETH_prices.merge(latest_ADA_prices, how='inner', left_on=["time"], right_on=["time"])
merged_data = merged_data.merge(latest_UNI_prices, how='inner', left_on=["time"], right_on=["time"])
merged_data = merged_data.merge(latest_DOGE_prices, how='inner', left_on=["time"], right_on=["time"])
merged_data['Total']= merged_data.sum(axis=1)

#Create Figure 8
plt.figure(8)
plt.plot(latest_ETH_prices['time'],latest_ETH_prices['close'], color = 'red', markevery=100, label="Etherium")
plt.plot(latest_BTC_prices['time'],latest_BTC_prices['close'], color = 'green', markevery=100, label="Bitcoin")
plt.plot(latest_ADA_prices['time'],latest_ADA_prices['close'], color = 'blue', markevery=100, label="Cardano")
plt.plot(latest_UNI_prices['time'],latest_UNI_prices['close'], color = 'yellow', markevery=100, label="Uniswap")
plt.plot(latest_DOGE_prices['time'],latest_DOGE_prices['close'], color = 'orange', markevery=100, label="Dogecoin")
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Cryptocurrency Prices - Logarithmic Scale')
plt.xticks(rotation = 45)
plt.yscale('log')
plt.legend()

#Create Figure 9
plt.figure(9)
plt.plot(latest_BTC_prices['time'],latest_BTC_prices['close'], color = 'green', markevery=100, label="Bitcoin")
plt.plot(merged_data['time'],merged_data['Total'], color = 'red', markevery=100, label="Top 4 Currencies excluding Bitcoin")
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Cryptocurrency Prices - Logarithmic Scale')
plt.xticks(rotation = 45)
plt.yscale('log')
plt.legend()

#Create Figure 10
plt.figure(10)
plt.bar(latest_BTC_prices['time'],latest_BTC_prices['close'], color = 'green', label="Bitcoin")
plt.bar(merged_data['time'],merged_data['Total'], color = 'red', label="Top 4 Currencies excluding Bitcoin", bottom = latest_BTC_prices['close'])
#Add Labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Cryptocurrency Prices - Logarithmic Scale')
plt.xticks(rotation = 45)
plt.legend()

plt.show()