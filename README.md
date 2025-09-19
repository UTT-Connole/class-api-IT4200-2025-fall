# class-api-IT4200-2025-fall
---
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

# open http://127.0.0.1:8000/mines



## Bulid as of latest commit by DaveTheFave is Runnable
Please be aware of the following problems that prevent running that needed to be fixed to run:
* Duplicate endpoints, either same name, or complete copied laying around after merge conflicts
* Duplicate function names, like `home()` has been used several times. This has been hotfixed with `home1(), home2()` and so forth. Recommend using unique function names.
* Otherwise normal python syntax errors. Remember CS1410 my dudes?
---
## UNLIVABLE REAL ESTATE – UNDERWATER EDITION
New endpoint includes totally-uninhabitable underwater properties.  
Scuba gear not included. Oxygen sold separately.  

How to run:  
source .venv/bin/activate  
pip install -r requirements.txt  
python app.py  
### open http://127.0.0.1:8000/api/underwater/properties  

## Recent Landing Page Updates (by Kasen)

- Added more GIFs to the landing page for extra fun and visual interest.
- Created a dedicated GIF container to organize and style the GIFs.
- Introduced a header section at the top of the page featuring an eye-catching GIF that covers the entire header area.
- Improved layout so the header GIF is flush with the top of the page (no gray space above).

Check out `templates/index.html` to see these changes in action!


## /randompkmon endpoint
This endpoint will direct you to a random pokemon listed on pokemon.com's website

## Pokémon

Pokémon is a media franchise created by Satoshi Tajiri and Ken Sugimori, first released by Nintendo, Game Freak, and Creatures in 1996. The franchise centers around fictional creatures called "Pokémon", which humans, known as Pokémon Trainers, catch and train to battle each other for sport.

### Main Concepts

- **Pokémon**: Creatures with various abilities, types, and evolutions. There are currently over 1,000 unique Pokémon species.
- **Types**: Each Pokémon has one or two types (such as Water, Fire, Grass, Electric, Psychic, etc.), which determine strengths and weaknesses in battles.
- **Battles**: Trainers use their Pokémon to battle others, using moves and strategies based on type advantages.
- **Evolution**: Many Pokémon can evolve into more powerful forms, often by leveling up, using special items, or meeting certain conditions.

### Popular Pokémon

- **Pikachu**: The franchise mascot, an Electric-type Pokémon.
- **Charizard**: A powerful Fire/Flying-type, final evolution of Charmander.
- **Bulbasaur, Squirtle, and Charmander**: The original starter Pokémon from the first games.

### Games

The main series consists of role-playing games (RPGs) where players travel through regions, catch Pokémon, defeat Gym Leaders, and challenge the Pokémon League. Notable games include:
- Pokémon Red/Blue/Yellow (Gen 1)
- Pokémon Gold/Silver/Crystal (Gen 2)
- Pokémon Ruby/Sapphire/Emerald (Gen 3)
- Pokémon Sword/Shield (Gen 8)
- Pokémon Scarlet/Violet (Gen 9)

### Other Media

- **Anime**: Follows Ash Ketchum and his friends as they travel the world, catch Pokémon, and compete in tournaments.
- **Trading Card Game**: A collectible card game where players build decks and battle.
- **Movies, Manga, and Merchandise**: Pokémon has a vast array of movies, comics, toys, and other products.

### Fun Facts

- The name "Pokémon" is a contraction of "Pocket Monsters" (ポケットモンスター).
- The franchise is one of the highest-grossing media franchises in the world.
- "Gotta Catch 'Em All!" is the iconic slogan.

For more information, visit the [official Pokémon website](https://www.pokemon.com/).


------------
Route "Gill"

We want another shrubbery.
A
A
A
A
A
A
A
A
A
MAKE IT BREAK PLZ :)


## /Client endpoint
This endpoint when called, will return the Browser and OS of the client calling the endpoint.
To implement this endpoint, it requires installing from requirements.txt
### To install requirments.txt
Run the following `pip install -r requirements.txt`

## /Dave endpoint
This endpoint will direct you to another random website

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

## /placeBetPOC endpoint
This is a proof of concept endpoint for placing bets. Eventually should be developed to use more variables to be more dynamic with other systems.
This endpoint takes betName and betOptions: a string for what the bet is about and a list of options for what players can bet on.
Currently assumes only 2 players will be betting.

## /Fortune endpoint (Bryson Francis)
Selects a predetermined fortune from a list of fortunes. Contains untold developer wisdom and mood readings

## /roll endpoint (Bryson Francis)
Rolls an "x" sided dice and returns the value of the rolled dice. It also returns an error if someone tries to roll a dice lower than 2.
## /Rock-Paper-Scissors Betting (/bet/rps)
Place a bet on rock, paper, or scissors and see if you win against the computer.

## /steal_yo_name endpoint


This endpoint will return one of 4 random names. Random name posibilty "La-a", "Abcde", "Quadraic", "Socrotent".


## /Skylands
This endpoint is broken and should be disregarded.

Not too hungry today


## /Weather-current
This give the current weather for St. George 

## /dallin
This endpoint gives you the option to delete the internet if you wish. 

## /weather
This endpoint returns a truely random weather condition. 

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

## /music
Gives a random music genre to listen to. Now added count to ask for multiple genres. If number exceeds list count, will just give the full list. If given no number, defaults to 1