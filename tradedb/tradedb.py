import sqlite3
import time
import json
import webbrowser
import tradequery

DATA_FOLDER = "D:\\development\\data\\"
DATABASE = "trades.db"
REPORT = "report.html"
TRADE = "trade.json"

def open_trade():
	trade = {}
	with open(TRADE) as file:
		trade = json.load(file)
	return trade

def write_trade(trade):
	with open(TRADE, 'w') as file:
		json.dump(trade, file, indent=2)

class Trades:

	def __init__(self):
		print(f"Database: {DATA_FOLDER + DATABASE}")
		self.conn = sqlite3.connect(DATA_FOLDER + DATABASE)
		self.cursor = self.conn.cursor()

		self.cursor.execute(
			"""CREATE TABLE IF NOT EXISTS trades (
				id INTEGER PRIMARY KEY, 
				ticker TEXT, 
				sector TEXT, 
				source_of_trade TEXT, 
				reasoning TEXT,
				technical_indicators TEXT,
				entry REAL,
				exit REAL,
				stop_loss REAL,
				risk REAL,
				reward REAL,
				actual_entry REAL,
				actual_exit REAL,
				profit_loss REAL,
				comments TEXT)""")

		self.conn.commit()

	def close(self):
		self.conn.close()

	def record(self):
		trade = open_trade()
		timestamp = int(time.time())
		self.cursor.execute(
			f"""INSERT INTO trades VALUES({timestamp}, '{trade['ticker']}', '{trade['sector']}', '{trade['source_of_trade']}', '{trade['reasoning']}', '{json.dumps(trade['technical_indicators'])}',
				{trade["entry"]}, {trade["exit"]}, {trade["stop_loss"]}, {trade["risk"]}, {trade["reward"]}, {trade["actual_entry"]}, {trade["actual_exit"]}, 
				{trade["profit_loss"]}, '{trade["comments"]}')""")
		self.conn.commit()
		return timestamp

	def delete(self, id):
		sql = f"DELETE FROM trades WHERE id = {id}"
		self.cursor.execute(sql)
		print(sql)
		self.conn.commit()

	def modify(self, id):
		trade = open_trade()
		sql = f"""
			UPDATE trades
			SET ticker='{trade['ticker']}',
				sector='{trade['sector']}',
				source_of_trade='{trade['source_of_trade']}',
				reasoning='{trade['reasoning']}',
				technical_indicators='{json.dumps(trade['technical_indicators'])}',
				entry={trade['entry']},
				exit={trade['exit']},
				stop_loss={trade['stop_loss']},
				risk={trade['risk']},
				reward={trade['reward']},
				actual_entry={trade['actual_entry']},
				actual_exit={trade['actual_exit']},
				profit_loss={trade['profit_loss']},
				comments='{trade['comments']}'
			WHERE id = {id}
		"""
		self.cursor.execute(sql)
		print(sql)
		self.conn.commit()

	def search(self, parameters):
		sql = """SELECT * FROM trades"""
		statements = tradequery.query(parameters)

		if (len(statements) > 0):
			sql += " WHERE " + ' AND '.join(statements)

		sql += " ORDER BY id DESC"

		print(sql)
		return sql

	def report(self, parameters):
		sql = self.search(parameters)

		html = """
			<html>
				<head>
					<style>
						table, td {
  							border: 1px solid black;
  							padding: 5px;
						}
						th {
							font-weight: black;
							border: 1px solid black;
  							padding: 5px;
						}
					</style>
				</head>
				<body>
					<table>
						<tr>
							<th>ID</th>
							<th>Ticker</th>
							<th>Sector</th>
							<th>Source</th>
							<th>Reasoning</th>
							<th>Technical Indicator</th>
							<th>Entry</th>
							<th>Exit</th>
							<th>Stop Loss</th>
							<th>Risk</th>
							<th>Reward</th>
							<th>Actual Entry</th>
							<th>Actual Exit</th>
							<th>Profit/Loss</th>
							<th>Comments</th>
						</tr>
		"""

		for row in self.cursor.execute(sql):
			html += "<tr>"

			for cell in row:
				html += f"<td>{cell}</td>"

			html += "</tr>"

		html += """
					</table>
				</body>
			</html>
		"""

		with open(DATA_FOLDER+REPORT, 'w') as file:
			file.write(html)

		webbrowser.open(DATA_FOLDER+REPORT, new=2)

