import curses

from snakegame.model.util import Point

char_map = {
    'snake_body': '@', 'snake_tail': 'o', 'snake_head': 'O', 'food': 'X',
    'horiz_border': '=', 'vert_border': '|'
}


def draw_game(window, map):
    window.clear()
    window = draw_game_border(window, map)
    window = draw_items(window, map)
    window = display_scores(window, map)
    return window


def draw_game_border(window, map):
    chars = {
        pos: char_map['vert_border']
        for pos in [Point(0, i) for i in range(1, map.dimension_max[0])]
    }
    chars.update({
        pos: char_map['vert_border']
        for pos in [
            Point(map.dimension_max[1], i) for i in range(1, map.dimension_max[0])
        ]
    })
    chars.update({
        pos: char_map['horiz_border']
        for pos in [Point(i, 0) for i in range(1, map.dimension_max[1])]
    })
    chars.update({
        pos: char_map['horiz_border']
        for pos in [
            Point(i, map.dimension_max[0]) for i in range(1, map.dimension_max[1])
        ]
    })

    for pos, char in chars.items():
        window.addch(pos.y, pos.x, char)
    window.refresh()
    return window


def draw_items(window, map):
    for i, snake in enumerate(map.snakes, start=1):
        chars = {}
        chars.update({pos: char_map['snake_body'] for pos in snake.body})
        chars.update({snake.head: char_map['snake_head']})
        for point, char in chars.items():
            window.addstr(point.y, point.x, char, curses.color_pair(i))
        window.addstr(snake.tail.y, snake.tail.x, char_map['snake_tail'], curses.color_pair(i%2 + 1))

    for food in map.food:
        chars = {}
        chars.update({food: char_map['food']})
        for point, char in chars.items():
            window.addstr(point.y, point.x, char)
    window.refresh()
    return window


def display_scores(window, map):

    for i, score in enumerate(map.score.values()):
        score_str = f"Snake {i}: {score}"
        window.addstr(map.dimension_max[1] + 2 + i, 1, score_str)
    window.refresh()

    return window
