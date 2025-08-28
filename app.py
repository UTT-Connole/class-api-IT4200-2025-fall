from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

@app.route('/brayden')
def brayden():
	return 'SupDudes'

if __name__ == '__main__':
	app.run(debug=True)
