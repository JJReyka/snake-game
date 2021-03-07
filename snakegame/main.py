import argparse
import asyncio
import curses
import logging

from snakegame.io import KeyReader
from snakegame.model import Game
from snakegame.model import Snake
from snakegame.model.util import chargroups, UP, DOWN, LEFT, RIGHT, Point

from snakegame.view.game_view import draw_game, display_scores




def main(stdscr):
    loop = asyncio.get_event_loop()
    curses.noecho()
    curses.cbreak()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Initialise game
    game = Game(dimensions=(12, 12))
    snake = Snake(name='snek1', start_points=[[3, 3], [3, 4], [3, 5]])
    game.add_snake(snake)
    snake = Snake(name='snek2', start_points=[[8, 8], [8, 7], [8, 6]])
    game.add_snake(snake)
    game.add_food(Point(6, 7))
    key_bindings = {}
    for chars, snake in zip(chargroups, game.snakes):
        for char, direction in zip(chars, [UP, LEFT, DOWN, RIGHT]):
            key_bindings[char] = (snake, direction)

    keyreader = KeyReader(snake_keys=key_bindings)
    loop.create_task(keyreader.get_keys(loop))
    loop.run_until_complete(update_and_draw(stdscr, game))

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


async def update_and_draw(win, map):
    while True:
        map.update()
        win = draw_game(win, map)
        win = display_scores(win, map)
        if not map.snakes:
            break
        await asyncio.sleep(1.0 / map.tick_rate)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug')

    logging.basicConfig(filename='game.log', level=logging.WARNING)
    curses.wrapper(main)









