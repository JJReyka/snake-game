import argparse
import asyncio
import curses
import logging

from snakegame.io import KeyReader
from snakegame.model import Game
from snakegame.model import Snake
from snakegame.model.util import key_groups, UP, DOWN, LEFT, RIGHT, Point

from snakegame.view.game_view import GameView


def main(stdscr):
    # Get the active event loop
    loop = asyncio.get_event_loop()

    # Change echoing settings and add custom colours for the player characters
    curses.noecho()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Initialise game with some defaults
    game = Game(dimensions=(12, 12))
    snake = Snake(name='snek1', start_points=[[3, 3], [3, 4], [3, 5]])
    game.add_snake(snake)
    snake = Snake(name='snek2', start_points=[[8, 8], [8, 7], [8, 6]])
    game.add_snake(snake)
    game.add_food(Point(6, 7))
    view = GameView(game=game)
    # Set up the key mappings
    key_bindings = {}
    for mapping, snake in zip(key_groups.values(), game.snakes):
        for key, direction in mapping.items():
            key_bindings[key] = (snake, direction)
    keyreader = KeyReader(snake_keys=key_bindings)

    # Start a task which reads input from stdin
    loop.create_task(keyreader.get_keys(loop))

    # Start the actual game loop
    loop.run_until_complete(view.update_and_draw(stdscr))

    # Return settings to normal
    curses.echo()
    curses.endwin()


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(filename='game.log', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='game.log', level=logging.WARNING)
    curses.wrapper(main)


if __name__ == "__main__":
    cli()








