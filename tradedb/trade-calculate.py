import math
import json
import tradedb

#VARIABLES

#Reward:Risk ratio
REWARD = 3
RISK = 1

#Account Balance
BALANCE = 50000

#Percentage of Account to Leverage
LEVERAGE_PERC = 5.0

#CODE STARTS HERE
TRADE = tradedb.open_trade()

max_trade_amount = BALANCE * (LEVERAGE_PERC / 100)
print(f"Max Amount Traded: ${round(max_trade_amount, 2)}")

shares = math.floor(max_trade_amount / TRADE['entry'])
print(f"SHARES: {shares}")

amount_spent = shares * TRADE['entry']
print(f"Amount Spent on Trade: ${round(amount_spent, 2)}")

reward = TRADE['exit'] - TRADE['entry']
print(f"REWARD: ${round(reward, 2)}")

reward_perc = reward / TRADE['entry'] * 100
print(f"Reward Perc: {round(reward_perc, 2)}%")

risk_perc = reward_perc * (RISK / REWARD )
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
TRADE["risk"] = RISK
TRADE["reward"] = REWARD
TRADE["actual_entry"] = 0
TRADE["actual_exit"] = 0
TRADE["profit_loss"] = 0

print(json.dumps(TRADE, indent=2))
tradedb.write_trade(TRADE)