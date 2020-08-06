import template
import webbrowser
import configuration
import wsb
import stockprofile
import stocktwits
import competitors

def screen(ticker):
	stock_profiles = []

	print('Fetching profile...')
	stock_profiles.append(stockprofile.build_profile(ticker))

	print('Fetching analyst feed...')
	price_analysis = stockprofile.get_analyst_feed(ticker)

	print('Fetching news feed...')
	news = stockprofile.get_news_feed(ticker)

	print('Processing news feed...')
	rendered_news = stockprofile.parse_news(news)
	stockprofile.build_bar_charts(news, configuration.DATA_FOLDER+'twits-sentiment.png')

	print('Fetching WSB submissions...')
	submissions = wsb.get_hot_submissions()

	print('Processing WSB submissions...')
	wsb_submissions=wsb.process_submissions(submissions, ticker, stock_profiles[0]['name'], configuration.DATA_FOLDER+'wsb-options.png', 
		configuration.DATA_FOLDER+'wsb-scores.png')

	print('Fetching Stock Twits...')
	twits = stocktwits.get_messages(ticker)

	print('Processing Stock Twits...')
	rendered_twits = stocktwits.process_messages(twits)
	stocktwits.build_bar_charts(twits, configuration.DATA_FOLDER+'twits-sentiment.png') 

	print('Fetching and processing competitors...')
	stock_profiles.extend(competitors.build_competitors_list(stock_profiles[0]['industry'], ticker))

	print('Building report...')

	# Rednder the html template with all the data
	rendered_html = template.get('screener.html').render(
		ticker=ticker, stocks=stock_profiles, news=rendered_news, price_analysis=price_analysis, wsb=wsb_submissions, twits=rendered_twits)
	rendered_html.encode('utf8')

	# Add the html file to data folder
	with open(configuration.DATA_FOLDER+'screener.html', 'w', encoding='utf8') as file:
		file.write(rendered_html)

	# Open the html file using the default web browser
	webbrowser.open(configuration.DATA_FOLDER+'screener.html', new=2)

