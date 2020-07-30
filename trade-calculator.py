import math

#VARIABLES

#Reward:Risk ratio
REWARD = 3
RISK = 1

#Account Balance
BALANCE = 50000

#Percentage of Account to Leverage
LEVERAGE_PERC = 5.0

#Stock Entry and Exit Targets
ENTRY = 319.65
EXIT = 326.45

#CODE STARTS HERE
max_trade_amount = BALANCE * (LEVERAGE_PERC / 100)
print(f"Max Amount Traded: ${round(max_trade_amount, 2)}")

shares = math.floor(max_trade_amount / ENTRY)
print(f"SHARES: {shares}")

amount_spent = shares * ENTRY
print(f"Amount Spent on Trade: ${round(amount_spent, 2)}")

reward = EXIT - ENTRY
print(f"REWARD: ${round(reward, 2)}")

reward_perc = reward / ENTRY * 100
print(f"Reward Perc: {round(reward_perc, 2)}%")

risk_perc = reward_perc * (RISK / REWARD )
print(f"Risk Perc: {round(risk_perc, 2)}%")

loss = ENTRY * (risk_perc / 100)
print(f"Loss Allowed: ${round(loss, 2)}")

stop_loss = ENTRY - loss
print(f"STOP LOSS: ${round(stop_loss, 2)}")

gain = (EXIT * shares) - amount_spent
print(f"GAIN: ${round(gain, 2)}")

loss = amount_spent - (stop_loss * shares)
print(f"LOSS: ${round(loss, 2)}")