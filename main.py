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

