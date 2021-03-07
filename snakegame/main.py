import argparse
import asyncio
import curses
import logging

from snakegame.io import KeyReader
from snakegame.model import Game
from snakegame.model import Snake
from snakegame.model.util import key_groups, Point, EXIT

from snakegame.view.game_view import GameView


def main(stdscr, speed, two_player):
    """Run the game

    Parameters
    ----------
    stdscr: curses.Window
        The window returned by curses.initscr()
    speed: str
        The speed to run the game at.
    two_player: bool
        1 or 2 player mode
    """
    # Get the active event loop
    loop = asyncio.get_event_loop()

    # Change echoing settings and add custom colours for the player characters
    curses.noecho()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    if two_player:
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    else:
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # Initialise game with some defaults
    tick_rate = {'fast': 4, 'normal': 2, 'slow': 1}
    game = Game(dimensions=(12, 12), tick_rate=tick_rate[speed])
    snake = Snake(name='snek1', start_points=[[3, 3], [3, 4], [3, 5]])
    game.add_snake(snake)
    if two_player:
        snake = Snake(name='snek2', start_points=[[7, 8], [7, 7], [7, 6]])
        game.add_snake(snake)
    game.add_food(Point(5, 6))
    view = GameView(game=game)
    # Set up the key mappings
    key_bindings = {}
    for mapping, snake in zip(key_groups.values(), game.snakes):
        for key, direction in mapping.items():
            key_bindings[key] = (snake, direction)
    keyreader = KeyReader(snake_keys=key_bindings, exit_key=EXIT, game=game)

    # Schedule a task which reads input from stdin and a task which updates
    # and draws the game state
    input_loop = loop.create_task(keyreader.get_keys(loop))
    draw_loop = loop.create_task(view.update_and_draw(stdscr))
    draw_loop.add_done_callback(lambda: input_loop.cancel())

    # Start the actual game loop
    loop.run_until_complete(draw_loop)

    # Return settings to normal
    curses.echo()
    curses.endwin()


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', action='store_true',
        help='Write debugging logs to "game.log"'
    )
    parser.add_argument(
        "--game-speed", type=str, choices=['fast', 'normal', 'slow'],
        default='normal', help='Sets the game speed'
    )
    parser.add_argument(
        "--2-player", action='store_true', help='Play a 2-player version',
        dest='two_player'
    )
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(filename='game.log', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='game.log', level=logging.WARNING)
    curses.wrapper(main, speed=args.game_speed, two_player=args.two_player)


if __name__ == "__main__":
    cli()








