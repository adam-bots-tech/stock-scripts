import template
import webbrowser
import configuration
import finviz
from finviz.screener import Screener
import re

TICKER = "TSLA"

#CODE BEGINS HERE
def build_profile(ticker, stock):
	return {
		'ticker': ticker,
		'name': stock['Company'],
		'pe': stock['P/E'],
		'eps': stock['EPS (ttm)'],
		'eps_q': stock['EPS next Q'],
		'mc': stock['Market Cap'],
		'forward_pe': stock['Forward P/E'],
		'income': stock['Income'],
		'sales': stock['Sales'],
		'52w': stock['52W Range'],
		'roe': stock['ROE'],
		'avg_vol': stock['Avg Volume'],
		'vol': stock['Volume']
	}

stock_profiles = []

# Determine what industry the stock is in so we can get competitors for comparison.
stock = finviz.get_stock(TICKER)
stock_profiles.append(build_profile(TICKER, stock))

screener_filter = "ind_" + re.sub(r'\W+', '', stock['Industry']).lower()

#Get the top five stocks in that industry
screened_stocks = Screener(filters=[screener_filter], table='Overview', order='-marketcap')

i = 0
for screened_stock in screened_stocks:
	i += 1

	if screened_stock['Ticker'] == TICKER:
		continue

	stock = finviz.get_stock(screened_stock['Ticker'])
	stock_profiles.append(build_profile(screened_stock['Ticker'], stock))

	if i > 5:
		break

rendered_html = template.get(configuration.INDUSTRY_SCREENER).render(
	ticker=TICKER, stocks=stock_profiles)

with open(configuration.DATA_FOLDER+configuration.SCREENER, 'w') as file:
	file.write(rendered_html)

webbrowser.open(configuration.DATA_FOLDER+configuration.SCREENER, new=2)

