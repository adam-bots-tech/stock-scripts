def query(parameters):
	statements = []
		
	if 'gain' in parameters.keys():
		if parameters['gain'] == True:
			statements.append("profit_loss >= 0")
		else:
			statements.append("profit_loss < 0")

	return statements