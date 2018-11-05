import pandas_datareader.data as web
import pandas as pd
import numpy as np
import os

def pull_data_from_av(tickers, data_type, start_date, end_date):
	data = pd.DataFrame()
	for ticker in tickers:
		quote = web.DataReader(ticker, data_type, start_date, end_date,  access_key=os.getenv('ALPHAVANTAGE_API_KEY'))
		quote['ticker'] = ticker
		data = pd.concat([data, quote])
	return data

def __add_ticker_names_to_df(tickers, data_frame):
	list_of_columns = ['returns','stdev','sharpe'] + sorted(tickers)
	data_frame = pd.DataFrame(data_frame.T,columns=list_of_columns)
	return data_frame

def simulation_without_active_management(table, num_of_portfolios, tickers):
	num_of_tickers = len(tickers)
	table.head()
	#calculate montly returns
	returns_montly = table.pct_change()
	returns_annual = returns_montly.mean()*12

	# get daily and covariance of returns of the stock
	cov_montly = returns_montly.cov()
	cov_annual = cov_montly * 12


	#Create empty dataframe
	portfolios = np.zeros((4+len(tickers)-1, num_of_portfolios))


	#Run simulations of portfolios with random weights
	for portfolio in range(num_of_portfolios):
		weights = weights = np.random.random(num_of_tickers)
		weights /= np.sum(weights)
		returns = np.dot(weights, returns_annual)
		volativity = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
		portfolios[0, portfolio] = returns
		portfolios[1, portfolio] = volativity
		portfolios[2, portfolio] = returns/volativity
		for weight in range(len(weights)):
			portfolios[weight+3, portfolio] = weights[weight]

	portfolios = __add_ticker_names_to_df(tickers, portfolios)
	return portfolios


def clean_table(data):
	#Add date field for easier handling and discard data which is not needed
	data['date'] = data.index
	data = data.filter(['date', 'ticker', 'adjusted close'], axis=1)

	#Clean table to easy to read format
	clean = data.set_index('date')
	table = clean.pivot(columns='ticker')
	table = table.replace(0, np.NaN).fillna(method='ffill')
	return table