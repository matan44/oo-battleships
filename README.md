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
I did not have enough time to add other tests.
These board unit test do show correct mocking.
They also show testing all the logic the board.py,
while not testing logic from other modules.
