import math
import json
import configuration

def position(ticker, entry, exit, balance, leverage):

	TRADE = {
	  "ticker": ticker,
	  "entry": entry,
	  "exit": exit,
	}

	#CODE STARTS HERE
	max_trade_amount = balance * (leverage / 100)
	print(f"Max Amount Traded: ${round(max_trade_amount, 2)}")

	shares = math.floor(max_trade_amount / TRADE['entry'])
	print(f"SHARES: {shares}")

	amount_spent = shares * TRADE['entry']
	print(f"Amount Spent on Trade: ${round(amount_spent, 2)}")

	reward = TRADE['exit'] - TRADE['entry']
	print(f"Reward: ${round(reward, 2)}")

	reward_perc = reward / TRADE['entry'] * 100
	print(f"Reward Perc: {round(reward_perc, 2)}%")

	risk_perc = reward_perc * (configuration.RISK / configuration.REWARD )
	print(f"Risk Perc: {round(risk_perc, 2)}%")

	loss = TRADE['entry'] * (risk_perc / 100)
	print(f"Loss Allowed: ${round(loss, 2)}")

	stop_loss = TRADE['entry'] - loss
	print(f"STOP LOSS: ${round(stop_loss, 2)}")

	gain = (TRADE['exit'] * shares) - amount_spent
	print(f"GAIN: ${round(gain, 2)}")

	loss = amount_spent - (stop_loss * shares)
	print(f"LOSS: ${round(loss, 2)}")

	print("\nTRADE JSON:\n")

	TRADE["stop_loss"] = stop_loss
	TRADE["risk"] = loss
	TRADE["reward"] = reward
	TRADE["shares"] = shares
	TRADE["cost"] = amount_spent

	print(json.dumps(TRADE, indent=2))