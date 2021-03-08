import unittest
from unittest import mock
from snakegame.model import Game, Snake
from snakegame.model.util import Point, DOWN, RIGHT, UP


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.snake = Snake(
            name='testsnake',
            start_points=[Point(i, 3) for i in range(2, 5)]
        )
        self.game.add_snake(self.snake)
        self.game.food = [Point(4, 5)]

    def test_boundary_collision(self):
        self.assertEqual(self.game.snakes, [self.snake])
        # Crash the snake into a wall
        for _ in range(6):
            self.game.update()

        self.assertEqual(self.game.snakes, [])

    @mock.patch.object(Game, 'add_food')
    def test_snake_food_tile(self, mk_add):
        # Mock the add_food method so we don't randomly add a new item
        self.snake.set_direction(DOWN)
        self.assertEqual(self.game.food, [Point(4, 5)])
        for _ in range(2):
            self.game.update()
        self.assertEqual(self.game.food, [])

        # Check the snake is set to grow next turn
        self.assertTrue(self.snake.grow)

    def test_snake_self_collision(self):
        # Loop an input snake around so it collides with itself in one update
        self.snake = Snake(
            name='testsnake',
            start_points=[Point(2, 3), Point(3, 3), Point(4, 3), Point(4, 4),
                          Point(3, 4)]
        )
        self.game.snakes = [self.snake]
        self.snake.set_direction(UP)
        self.game.update()
        self.assertEqual(self.game.snakes, [])

    def test_two_player_collision(self):
        # Crash snake1 into snake2
        self.snake2 = Snake(
            name='testsnake2',
            start_points=[Point(6, 6), Point(6, 5), Point(6, 4)]
        )
        self.game.add_snake(self.snake2)
        self.assertEqual(len(self.game.snakes), 2)
        for i in range(2):
            self.game.update()
        self.assertEqual(len(self.game.snakes), 1)

    def test_two_player_head_collision(self):
        self.snake2 = Snake(
            name='testsnake2',
            start_points=[Point(7, 3), Point(6, 3), Point(5, 3)]
        )
        self.game.add_snake(self.snake2)
        self.game.update()
        self.assertEqual(self.game.snakes, [])

    def test_tail_bite(self):
        self.snake2 = Snake(
            name='testsnake2',
            start_points=[Point(6, 5), Point(6, 4), Point(6, 3)]
        )
        self.game.add_snake(self.snake2)
        for i in range(2):
            self.game.update()
        # Check p2 lost a piece
        self.assertEqual(len(self.game.snakes[0].points), 3)
        self.assertEqual(len(self.game.snakes[1].points), 2)
        # Avoid crashing!
        self.snake2.set_direction(RIGHT)
        self.game.update()
        # Check p1 gained one
        self.assertEqual(len(self.game.snakes[0].points), 4)
        self.assertEqual(len(self.game.snakes[1].points), 2)
