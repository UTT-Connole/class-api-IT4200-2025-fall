from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'
@app.route('/heather')
def home():
	return 'Hello!'
@app.route('/space-facts')
def space_facts():
    facts = [
        {"fact": "A day on Venus is longer than a year on Venus."},
        {"fact": "Neutron stars can spin 600 times per second."},
        {"fact": "Saturn could float in water because it’s mostly gas."},
        {"fact": "The footprints on the Moon will likely last millions of years."},
        {"fact": "Jupiter has 95 known moons as of 2025."}
    ]
    return jsonify(random.choice(facts))

if __name__ == '__main__':
	app.run(debug=True)
