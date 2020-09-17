import template
import webbrowser
import configuration
import stockprofile
import stocktwits
import competitors
import alphaadvanage
import technical_analysis
import brokerage

def help():
	print('screen(ticker)')

def screen(ticker):
	stock_profiles = []

	print('Fetching profile...')
	stock_profiles.append(stockprofile.build_profile(ticker, configuration.DATA_FOLDER))

	# Add description and bid ask prices
	profile = alphaadvanage.add_description_to_profile(stock_profiles[0], ticker, configuration.ALPHA_API, configuration.DATA_FOLDER)

	print('Fetching analyst feed...')
	price_analysis = stockprofile.get_analyst_feed(ticker, configuration.DATA_FOLDER)

	print('Fetching news feed...')
	news = stockprofile.get_news_feed(ticker, configuration.DATA_FOLDER)

	print('Processing news feed...')
	rendered_news = stockprofile.parse_news(news)
	stockprofile.build_bar_charts(news, configuration.DATA_FOLDER+'news-sentiment.png')

	print('Fetching technical analysis...')
	b = brokerage.Brokerage(True, configuration.ALPACA_KEY_ID, configuration.ALPACA_SECRET_KEY,configuration.DATA_FOLDER)
	tech = technical_analysis.analyze(ticker, b)

	print('Fetching Stock Twits...')
	twits = stocktwits.get_messages(ticker, configuration.DATA_FOLDER)

	print('Processing Stock Twits...')
	rendered_twits = stocktwits.process_messages(twits)

	print('Fetching and processing competitors...')
	stock_profiles.extend(competitors.build_competitors_list(stock_profiles[0]['industry'], ticker, configuration.DATA_FOLDER))

	print('Building quarterly finacials chart...')
	alphaadvanage.create_quarterly_financials_chart(ticker, configuration.DATA_FOLDER+'quarterly-reports.png', configuration.ALPHA_API, configuration.DATA_FOLDER)

	print('Building report...')

	# Rednder the html template with all the data
	rendered_html = template.get('screener.html').render(
		ticker=ticker, stocks=stock_profiles, news=rendered_news, price_analysis=price_analysis, twits=rendered_twits, tech=tech)
	rendered_html.encode('utf8')

	# Add the html file to data folder
	with open(configuration.DATA_FOLDER+'screener.html', 'w', encoding='utf8') as file:
		file.write(rendered_html)

	# Open the html file using the default web browser
	webbrowser.open(configuration.DATA_FOLDER+'screener.html', new=2)