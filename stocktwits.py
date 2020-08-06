import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

def get_messages(ticker):
	resp = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json')
	return resp.json()['messages'];

def process_messages(messages):
	twits = []
	for message in messages:
		twits.append(message['body'])
	return twits

def build_bar_charts(messages, chart_path):
	twits_sentiment=[0.0,0.0,0.0,0.0]
	analyzer = SentimentIntensityAnalyzer()
	news_sentiment_labels=['Negative', 'Neutral', 'Positive', 'Mixed']

	for message in messages:
		scores = analyzer.polarity_scores(message)
		twits_sentiment[0] += scores['neg'] 
		twits_sentiment[1] += scores['neu'] 
		twits_sentiment[2] += scores['pos'] 
		twits_sentiment[3] += scores['compound']

	plt.style.use('ggplot')
	plt.bar([i for i, _ in enumerate(twits_sentiment)], twits_sentiment, color='purple')
	plt.xlabel("Sentiment")
	plt.ylabel("Polarity Scores")
	plt.title("Stock Twits Sentiment Analysis")
	plt.xticks([i for i, _ in enumerate(news_sentiment_labels)], news_sentiment_labels)
	plt.savefig(chart_path)
	plt.close()
