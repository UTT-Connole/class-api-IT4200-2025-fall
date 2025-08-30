from flask import Flask, render_template, request, jsonify
import random
import json
from user_agents import parse
from datetime import date

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

if __name__ == '__main__':
	app.run(debug=True)