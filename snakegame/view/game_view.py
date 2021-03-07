import asyncio
import curses

from snakegame.model.util import Point

char_map = {
    'snake_body': '@', 'snake_tail': 'o', 'snake_head': 'O', 'food': 'X',
    'horiz_border': '=', 'vert_border': '|'
}


class GameView:

    def __init__(self, game):
        self.snake_colour = {}
        for i, snake in enumerate(game.snakes, start=1):
            self.snake_colour[snake] = i
        self.game = game

    async def update_and_draw(self, win):
        while True:
            self.game.update()
            win = self.draw_game(win, self.game)
            if not self.game.snakes:
                break
            await asyncio.sleep(1.0 / self.game.tick_rate)

    def draw_game(self, window, game):
        window.clear()
        window = self.draw_game_border(window, game)
        window = self.draw_items(window, game)
        window = self.display_scores(window, game)
        return window

    def draw_game_border(self, window, game):
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

        for i, score in enumerate(game.score.values()):
            score_str = f"Snake {i}: {score}"
            window.addstr(game.dimension_max[1] + 2 + i, 1, score_str)
        window.refresh()

        return window
