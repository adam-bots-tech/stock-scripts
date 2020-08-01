import os
from jinja2 import Environment, FileSystemLoader

def get(filename):
	current_directory = os.path.dirname(os.path.abspath(__file__))
	env = Environment(loader=FileSystemLoader(current_directory))

	return env.get_template(filename)