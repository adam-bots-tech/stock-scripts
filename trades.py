import math
import json
import trade_journal
import configuration
import technical_analysis
import brokerage
import trade
from datetime import datetime

def help():
	print('gain(price, gain_perc)')
	print('loss(price, gain_perc)')
	print('gain_perc(entry, exit)')
	print('position(entry, exit, balance)')
	print('create(ticker, entry, exit, stop_loss, expiration, sell_at_end_of_day, notes)')

def gain(price, gain_perc):
	return price + (price * gain_perc)

def loss(price, gain_perc):
	return price - (price * gain_perc)

def gain_perc(entry, exit):
	return ((exit - entry) / entry * 100) / 100

def position(entry, exit, balance):

	REWARD = 3
	RISK = 1

	#CODE STARTS HERE
	max_trade_amount = balance
	print(f"Max Amount Traded: ${round(max_trade_amount, 2)}")

	shares = math.floor(max_trade_amount / entry)
	print(f"SHARES: {shares}")

	amount_spent = shares * entry
	print(f"Amount Spent on Trade: ${round(amount_spent, 2)}")

	reward = exit - entry
	print(f"Reward: ${round(reward, 2)}")

	reward_perc = reward / entry * 100
	print(f"Reward Perc: {round(reward_perc, 2)}%")

	risk_perc = reward_perc * (RISK / REWARD )
	print(f"Risk Perc: {round(risk_perc, 2)}%")

	loss = entry * (risk_perc / 100)
	print(f"Loss Allowed: ${round(loss, 2)}")

	stop_loss = entry - loss
	print(f"STOP LOSS: ${round(stop_loss, 2)}")

	gain = (exit * shares) - amount_spent
	print(f"GAIN: ${round(gain, 2)}")

	loss = amount_spent - (stop_loss * shares)
	print(f"LOSS: ${round(loss, 2)}")

def create(ticker, entry, exit, stop_loss, expiration, sell_at_end_of_day, notes):
	j = trade_journal.TradeJournal(configuration.TRADE_JOURNAL_TITLE)
	j.bootstrap()
	b = brokerage.Brokerage(True, configuration.ALPACA_KEY_ID, configuration.ALPACA_SECRET_KEY, configuration.DATA_FOLDER)
	t = trade.Trade(datetime.timestamp(datetime.now()), ticker, 0.0, 0.0, 0.0, exit, entry, stop_loss, 0.0, 0.0, 'QUEUED', '', '', 'long', 0, expiration)
	metadata = json.dumps(technical_analysis.analyze(ticker, b))

	count = 0
	for row in j.journal[0].getRows():
		if row[0] != '':
			count += 1
		else:
			break

	j.create_queued_trade(count + 1, ticker, 'long', entry, exit, stop_loss, notes, expiration, metadata, sell_at_end_of_day)
	print("Trade Created.")
