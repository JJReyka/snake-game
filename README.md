SnakeGame
---------
A basic implementation of the mobile game snake
in python using curses to render the game in the terminal.
Ideally this will be upgraded so I can try out PyGame!

Installing
----------
- Requirements: python 3.8+
- Clone the repository with `git clone git@github.com:JJReyka/snake-game.git`
- Enter the newly created directory and install with `pip install .` 
- Run the game with `snake_game`, try `snake_game --help` for additional options (game speed, 2 player)
- If you see a warning on install saying `The script is installed in <directory name>, which is not in PATH` 
  you may have to run the game with `python -m snakegame.main` instead.
  
Controls
--------
w,a,s,d - move (p1)

i,j,k,l - move (p2)

q - quit

space - pause

Tested on Ubumtu and MacOS.
