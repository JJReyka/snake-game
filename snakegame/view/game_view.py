import asyncio
import curses

from snakegame.model.util import Point

char_map = {
    'snake_body': '@', 'snake_tail': 'o', 'snake_head': 'O', 'food': 'X',
    'horiz_border': '=', 'vert_border': '|'
}


class GameView:
    """A class which draws the current game state to screen"""

    def __init__(self, game):
        """Get a reference to the game itself and set colours"""
        self.snake_colour = {}
        for i, snake in enumerate(game.snakes, start=1):
            self.snake_colour[snake] = i
        self.game = game

    async def update_and_draw(self, win):
        """Update the game model and draw the current state at a frequency
        determined by the tick rate.

        Parameters
        ----------
        win: curses.Window
            The main window
        """
        while True:
            self.game.update()
            win = self.draw_game(win, self.game)
            if not self.game.snakes:
                break
            await asyncio.sleep(1.0 / self.game.tick_rate)

    def draw_game(self, window, game):
        """Draw the current game state.

        Parameters
        ----------
        win: curses.Window
            The main window
        """
        window.clear()
        window = self.draw_game_border(window, game)
        window = self.draw_items(window, game)
        window = self.display_scores(window, game)
        return window

    def draw_game_border(self, window, game):
        """Draw the border of the game area

        Parameters
        ----------
        window: curses.Window
            The main window
        """
        chars = {
            pos: char_map['vert_border']
            for pos in [Point(0, i) for i in range(1, game.dimension_max[0])]
        }
        chars.update({
            pos: char_map['vert_border']
            for pos in [
                Point(game.dimension_max[1], i) for i in range(1, game.dimension_max[0])
            ]
        })
        chars.update({
            pos: char_map['horiz_border']
            for pos in [Point(i, 0) for i in range(1, game.dimension_max[1])]
        })
        chars.update({
            pos: char_map['horiz_border']
            for pos in [
                Point(i, game.dimension_max[0]) for i in range(1, game.dimension_max[1])
            ]
        })

        for pos, char in chars.items():
            window.addch(pos.y, pos.x, char)
        window.refresh()

        return window

    def draw_items(self, window, game):
        """Draw the snakes and other items

        Parameters
        ----------
        window: curses.Window
            The main window
        """
        for snake in game.snakes:
            chars = {}
            chars.update({pos: char_map['snake_body'] for pos in snake.body})
            chars.update({snake.head: char_map['snake_head']})
            for point, char in chars.items():
                window.addstr(
                    point.y, point.x, char,
                    curses.color_pair(self.snake_colour[snake])
                )
            window.addstr(
                snake.tail.y, snake.tail.x, char_map['snake_tail'],
                curses.color_pair(
                    self.snake_colour[snake] % len(self.snake_colour) + 1
                )
            )

        for food in game.food:
            chars = {}
            chars.update({food: char_map['food']})
            for point, char in chars.items():
                window.addstr(point.y, point.x, char)
        window.refresh()
        return window

    def display_scores(self, window, game):
        """Display  scores below the game area

        Parameters
        ----------
        window: curses.Window
            The main window
        """
        for i, score in enumerate(game.score.values()):
            score_str = f"Snake {i}: {score}"
            window.addstr(game.dimension_max[1] + 2 + i, 1, score_str)
        window.refresh()

        return window
