import math
import json

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