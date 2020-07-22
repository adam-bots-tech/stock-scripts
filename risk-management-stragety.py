import random
import time

#This script can be used to test a risk management stragety.
#each trade in the series. The script performs a series of trades, with each trade being a series of the simulated candlesticks. The candlesticks are generated until
#the price target or the stop loss for the trade is reached.

#Each candlestick is created by a weighted dice roll determing whether or not the candlestick represents a loss or gain.
#The weight of the dice roll for a loss or gain and the range of the price fluxation per each candlestick
#can be configured to create different conditions of market volatility.

#To use the script, simply alter the constants below to configure the simulation and then run the script.

#TRADES
#Number of trades in a series
NUM_OF_TRADES = 100
#Number of series to runs
NUM_OF_SERIES = 10

#RISK MANAGEMENT STRAGETY
#Reward:Risk ratio
REWARD = 6.0
RISK = 2.0

#ACCOUNT MANAGEMENT
BASE_ACCOUNT_BALANCE = 5000
MAX_PERCENTAGE_OF_ACCOUNT_PER_TRADE = 50.0

#VOLATILITY OF CANDLESTICKS
#Chance of a gain or loss occuring for each candlestick's dice roll. Both numbers should equal 100.0
# If 50.0 and 50.0, then the market is kangaroo or flat.
# If 70.0 and 30.0, then the market is on a bullish trend.
# If 30.0 and 70.0, then the market is on a bearish trend.
CHANCE_OF_GAIN = 55.0
CHANCE_OF_LOSS = 45.0
#Volatility of price movement for the gain or loss of a candlestick. 
#What is the max percentage a price can move, in either direction, per candlestick?
CANDLESTICK_FLUX = 1.0

#STOCK
BASE_STOCK_PRICE = 20.0

####### CODE STARTS HERE #########

random.seed(time.time())

class Candlestick:
	def __init__(self, stock_price):
		self.stock_price = stock_price

	def roll(self):
		roll = random.randint(1, 100)
		price_increment = self.stock_price * ((random.randint(1, CANDLESTICK_FLUX * 100)) / 100) / 100

		if roll >= (100 - CHANCE_OF_GAIN):
			self.stock_price += price_increment
		elif roll <= (100 - CHANCE_OF_LOSS):
			self.stock_price -= price_increment

		return self.stock_price


class Trade:
	def __init__(self, shares):
		self.shares = shares
		self.candlesticks = 0
		self.gain = False
		self.closed = False
		self.sale_price = 0
		self.price_change_percentage = 0.0
		self.price_target = BASE_STOCK_PRICE + (BASE_STOCK_PRICE * (REWARD / 100))
		self.stop_loss = BASE_STOCK_PRICE - (BASE_STOCK_PRICE * (RISK / 100))

	def check_candlestick(self, candlestick):
		self.candlesticks += 1
		if (candlestick.stock_price >= self.price_target):
			self.gain = True
			self.closed = True
			self.sale_price = candlestick.stock_price
			self.price_change_percentage = ((self.sale_price - BASE_STOCK_PRICE) / BASE_STOCK_PRICE) * 100
		elif (candlestick.stock_price <= self.stop_loss):
			self.gain = False
			self.closed = True
			self.sale_price = candlestick.stock_price
			self.price_change_percentage = -((BASE_STOCK_PRICE - self.sale_price) / BASE_STOCK_PRICE) * 100
		
class Account:
	def __init__(self):
		self.balance = BASE_ACCOUNT_BALANCE
		self.trades = []

	def take_tendies(self, trade):
		self.trades.append(trade)
		self.balance += (trade.sale_price * trade.shares)

	def create_trade(self):
		max_trade_amount = self.balance * (MAX_PERCENTAGE_OF_ACCOUNT_PER_TRADE / 100)

		shares_to_buy = max_trade_amount / BASE_STOCK_PRICE
		if (self.balance - (shares_to_buy * BASE_STOCK_PRICE) <= 0):
			return False
		else:
			self.balance -= (shares_to_buy * BASE_STOCK_PRICE)
			return Trade(shares_to_buy)

	def get_account_change(self):
		return ((self.balance - BASE_ACCOUNT_BALANCE) / BASE_ACCOUNT_BALANCE) * 100

series = []

for series_num in range(1, NUM_OF_SERIES + 1):
	print(f"Series {series_num} Started.")
	account = Account()
	print(f"\tAccount Opened: ${account.balance}")

	for trade_num in range(1, NUM_OF_TRADES + 1):

		trade = account.create_trade()

		# We cannot create new trades if the account balance is zero or below
		if (trade == False):
			break

		stock_price = BASE_STOCK_PRICE

		while trade.closed == False:
			candlestick = Candlestick(stock_price)
			stock_price = candlestick.roll()
			trade.check_candlestick(candlestick)

		print(f"\t\tTrade Completed (Sale Price: ${round(trade.sale_price, 3)}, Shares: {round(trade.shares, 2)}, Price Change: {round(trade.price_change_percentage, 2)}%, Candlesticks: {trade.candlesticks})")
		account.take_tendies(trade)

	series.append(account)
	print(f"\tAccount Closed: ${round(account.balance, 2)}")
	print(f"Series {series_num} Finished.")

print("\nSERIES LIST\n")

for account in series:
	print(f"\tAccount Balance: ${round(account.balance, 2)}")
	print(f"\tAccount Change: {round(account.get_account_change(), 2)}%")
	print(f"\tTotal Trades: {len(account.trades)} \ {NUM_OF_TRADES}\n")
