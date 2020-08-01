import template
import webbrowser

TICKER = "TSLA"

# CODE BEGINS HERE
DATA_FOLDER = "D:\\development\\data\\"
REPORT = "screener.html"

rendered_html = template.get(REPORT).render(
	ticker=TICKER)

with open(DATA_FOLDER+REPORT, 'w') as file:
	file.write(rendered_html)

webbrowser.open(DATA_FOLDER+REPORT, new=2)

