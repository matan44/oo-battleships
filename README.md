Requirements:

Standard installation of python 3

To run the game:

`python -c "from battleships import game; game.Game().play()"`

Example Input and Output:

```
Board dimensions: (Format X Y, e.g. 3 C): 3 C
Number of ships per player: 1
Ships coordinates: (Format TYPE LENGTH HEIGHT XY, e.g. Q 1 1 A1): Q 1 1 A1
Ships coordinates: (Format TYPE LENGTH HEIGHT XY, e.g. Q 1 1 A1): Q 1 1 A1
Player 1's turn
Player 1 target coordinates (Format XY, e.g. A4): A1
Result: hit
Player 1's turn
Player 1 target coordinates (Format XY, e.g. A4): A2
Result: miss
Player 2's turn
Player 2 target coordinates (Format XY, e.g. A4): A1
Result: hit
Player 2's turn
Player 2 target coordinates (Format XY, e.g. A4): A1
Result: hit
Player 2 wins

```

To run behavioural tests:

`python -m unittest tests/behaviour_tests/playing_game_test.py`

To run unit tests tests:

`python -m unittest tests/unit_tests/model/board_test.py`


I wrote the behavioural tests for TDD. I did not have time to go back and polish them.

I only added unit test coverage to the board model.
I did not have enough time for more.
These board unit test do show correct mocking.
They also show testing all the logic the board.py,
while not testing logic from other modules.

### Brief explanation of assumptions
From the requirement to not use external libraries I concluded that you were only interested in a working game.
I assumed that fancy visualizations (with pygame maybe?), a webserver and database persistence
would have been unwanted excrescences.

And I didn't have time for anything further anyway :)

There are opportunities for optimisations
(example of low hanging fruit is that every access to Ship.is_destroyed
always checks all the ship's cells).

But I prioritised simplicity and cleanliness over optimisation, as I would in a production environment.

For the ship size and coordinates input for each player,
I deviated slightly from the Sample Input in the pdf instructions

There is no step for getting the finite missile number from the user. I put in a default of 99.


### Brief explanation of the design

- The game object holds two players.
- Each player has a board
- I went back and forth about whether the boards should be attached to the players or to the game object.
- I ultimately decided that attaching a board to each player was more elegant 
- The board has a list of lists representing its cells
- The cells are initially all None
- Before adding a ship the board checks that it would fit
- When adding a ship, the ship's cell are added to the board's cells
- At the end of each turn, each games checks whether the current player should go again
- At the end of each turn the games also checks whether either player won
