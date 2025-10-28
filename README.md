# class-api-IT4200-2025-fall
---
## The Coding Commandments

1. Thou shalt not set before the API any emojis, nor bow down unto them.
1. Honor thy professor, and submit to his benevolent dominion over this work.
1. Thou shalt not comment out code; thou shalt purge it utterly.
1. Thou shalt not duplicate endpoints, lest confusion multiply in the land.
1. Thou shalt keep the tests within the tests/ folder, and tend them with diligence.
1. Thou shalt not lay heavy burdens upon the tests; keep them swift of foot and free of sloth.

---
## Dockerfile Config Instructions

1. Install Docker [Here](https://www.docker.com/)
2. Make sure the user running Docker has permissions to run Docker
3. Navigate to this repo directory and run `docker build -t api_image .`
4. Then run `docker run -d -p 8000:8000 --name api_container api_image`
5. From any browser, access [http://localhost:8000](http://localhost:8000)

You should be able to access the landing page, and access the rest of our endpoints.

## Pylint:
Pylint is the tool that will check for sins committed against the Coding Commandments every time you push or pull code. 

## What is .pylintrc?
The .pylintrc file is the configuration file for our Pylint. 
It tells Pylint which rules to check, ignore, or adjust. 
This will be our “rules list”/"coding commandments".

Please update the README when checks are added to the pylint code:
* Missing or extra spaces
* Unused variables or imports
* Code that doesn’t follow standard Python style
* Potential bugs or bad practices
  
Run pylint yourself to test your code like so (This tests the app.py and code in the test folder):
```
pylint app.py test
```

## DYLAN's MINES GAMBLING GAME W UI
Run this really cool mine game.
Gamble your life away.

99% quit before they hit it big!!!

How to run:
```
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
open http://127.0.0.1:8000/mines

## UNLIVABLE REAL ESTATE – UNDERWATER EDITION
New endpoint includes totally-uninhabitable underwater properties.  
Scuba gear not included. Oxygen sold separately.  

How to run:  
source .venv/bin/activate  
pip install -r requirements.txt  
python app.py  
### open http://127.0.0.1:8000/api/underwater/properties  


## /randompkmon endpoint
This endpoint will direct you to a random pokemon listed on pokemon.com's website

## /Client endpoint
This endpoint when called, will return the Browser and OS of the client calling the endpoint.
To implement this endpoint, it requires installing from requirements.txt
### To install requirments.txt
Run the following `pip install -r requirements.txt`

## /Kasen endpoint
This endpoint is a new webpage that has a few gifs. I added buttons that go back and forth to each website. (I did this because I got bored)

## /dadJokes 
This endpoint will deliver a dad joke from a selection of three

## /Theisen Endpoint(dadJokeGenerator)
This endpoint will return one of 5 dad jokes listed.

## /magic8ball endpoint
This endpoint will return a random magic 8 ball message string. Possible messages consist of 3 "yes" answers, 2 "unsure" answers, and 3 "no" answers.

Blackjack Endpoint
This endpoint deals two cards to the player and dealer, calculates scores, and returns a winner.
Roulette Endpoint
This endpoint simulates a single spin of a European roulette wheel and returns the result.

## /generatePassword endpoint
This endpoint generates a random password with a set length and cmplexity level.
2 arguments: Length, Complexity
Length: A number for how many characters long the password will be.
Complexity: Basic, Simple, or Complex are the only valid options. Basic is only lowercase letters. Simple is lowercase letters and numbers. Complex is Lower and Uppercase letters, numbers, and symbols.

## /bingo endpoint
This endpoint generates a 5x5 bingo card that is a list of dictionaries with random bingo numbers. 
Each dictionary is a cell in the bingo card, storing the value and if the cell is marked.
Every 5 cells increases the range of possible values by 15.
Center space is always "FREE" and always marked.

## /double_or_nothing
Endpoint that has a 50/50 chance of doubling your money, or making you lose it all.
Enter amount argument by adding ?amount=<number> in endpoint url.

## /Fortune endpoint (Bryson Francis)
Selects a predetermined fortune from a list of fortunes. Contains untold developer wisdom and mood readings

## /roll endpoint (Bryson Francis)
Rolls an "x" sided dice and returns the value of the rolled dice. It also returns an error if someone tries to roll a dice lower than 2.
## /Rock-Paper-Scissors Betting (/bet/rps)
Place a bet on rock, paper, or scissors and see if you win against the computer.
## / Slot Machine endpoint
- Virtual slot machine with three random symbols.
- Payout rules:
  - 3 matching symbols: 10× your bet
  - 2 matching symbols: 3× your bet
  - No matches: 0 payout

## /steal_yo_name endpoint
This endpoint will return one of 4 random names. Random name posibilty "La-a", "Abcde", "Quadraic", "Socrotent".

## /random-weather
This endpoint returns a truely random weather condition. 

## /hazardous-conditions
This endpoint calls the /random-weather endpoint, and decides if it is a hazardous condition or not. It returns the results. 

## /current-weather
This give the current weather for St. George using the Open-Meteo API. 

## /campus-locations
Returns a random location on the Utah Tech Campus 

## /charger-facts
is a page that talks about the 1969 dodge charger and returns cool stuff
ex. The 1969 Dodge Charger is an iconic American muscle car known for its aggressive styling and powerful performance.
ex. It features a distinctive "coke bottle" body shape with hidden headlights and a full-width grille.
ex. The 1969 model year introduced the "R/T" (Road/Track) performance package for even greater speed and handling.
ex. Today, the 1969 Dodge Charger is a highly sought-after collector's car, celebrated for its style and performance.

## /dinner
This endpoint helps you decide what to eat for dinner!  
When called, it returns a random dinner suggestion from a list of popular options.  
You might get pizza, tacos, sushi, or something else tasty.  
Great for those nights when you can't make up your mind.  
Just visit `/dinner` and let fate choose your meal.  
Perfect for students, families, or anyone feeling indecisive!

## /fav_quote
Returns a quote
A few of the favorites

## /numberguesser - Number Guesser
This endpoint is a simple game that allows you to guess a randomly generated number between 1 and 10. The endpoint accepts POST with the users guess and returns a JSON if you won or lost. 

You can test this endpoint like so: curl -X POST http://127.0.0.1:5000/numberguesser -d "guess=5"

## /gatcha
Returns random results from a gatcha game

## /add_chips
Adds three different chips of different value to a currently unused list.

## /jukebox
Music endpoint was deleted, so the new latest and greatest version is here, jukebox. Simplified to return a random song with some data points including artist, genre, and release date.

## Properties endpoints

- `GET /api/chernobyl/properties?limit=N`
- `GET /api/mars/properties?limit=N`

`limit` is optional. If provided, it returns only the first `N` properties (clamped to available items).
If `limit` is not an integer, the API returns HTTP 400.
