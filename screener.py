import template
import webbrowser
import configuration

TICKER = "TSLA"

# CODE BEGINS HERE

rendered_html = template.get(configuration.SCREENER).render(
	ticker=TICKER)

with open(configuration.DATA_FOLDER+configuration.SCREENER, 'w') as file:
	file.write(rendered_html)

webbrowser.open(configuration.DATA_FOLDER+configuration.SCREENER, new=2)

