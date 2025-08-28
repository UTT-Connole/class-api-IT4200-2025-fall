from flask import Flask

app = Flask(__name__)

@app.route('/gill')
def home():
	return 'my test app'

if __name__ == '__main__':
	app.run(debug=True)
