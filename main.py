import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import requests

#2  Importing Data

#2a Retreive Data fom online APIs
#Example 1
response = requests.get('https://api.github.com/events')
print(response)

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
