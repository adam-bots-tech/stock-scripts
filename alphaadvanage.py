import requests
import configuration
import matplotlib.pyplot as plt
import numpy as np
import cache

def add_bid_ask_to_profile(stock, ticker):

	def response():
		return requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={configuration.ALPHA_API}')

	fileCache = cache.get_cache('TIME_SERIES_INTRADAY')
	resp = fileCache.get(key=ticker, createfunc=response)
	json = resp.json()

	for key in json['Time Series (5min)']:
		stock['bid'] = json['Time Series (5min)'][key]['3. low']
		stock['ask'] = json['Time Series (5min)'][key]['2. high']
		break

	return stock

def add_description_to_profile(stock, ticker):
	def response():
		return requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&interval=5min&apikey={configuration.ALPHA_API}')

	fileCache = cache.get_cache('OVERVIEW')
	resp = fileCache.get(key=ticker, createfunc=response)

	stock['description']=resp.json()['Description']
	return stock

def create_quarterly_financials_chart(ticker, chart_path):
	date = []
	revenue = []
	profit = []

	def response():
		return requests.get(f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&interval=5min&apikey={configuration.ALPHA_API}')

	fileCache = cache.get_cache('INCOME_STATEMENT')
	resp = fileCache.get(key=ticker, createfunc=response)

	json = resp.json()

	i = 0
	for report in json['quarterlyReports']:
		i += 1
		date.append(report['fiscalDateEnding'])
		revenue.append(int(report['totalRevenue']))
		profit.append(int(report['grossProfit']))
		if i >= 8:
			break

	x = np.arange(len(date))
	ax = plt.subplot(1,1,1)
	w = 0.3
	plt.xticks(x + w /2, date, rotation='vertical')
	rev =ax.bar(x, revenue, width=w, color='b', align='center')
	pro =ax.bar(x + w, profit, width=w,color='g',align='center')
	ax.xaxis_date()
	plt.legend([rev, pro],['Revenue', 'Profit'])
	plt.title("Quarterly Financial Reports")
	plt.savefig(chart_path)
	plt.close()

