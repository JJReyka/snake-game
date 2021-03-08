import unittest

from snakegame.model import Snake, Point
from snakegame.model.util import LEFT, RIGHT, UP


class TestSnake(unittest.TestCase):

    def setUp(self) -> None:
        # A snake facing right
        self.snake = Snake(
            name='testsnake',
            start_points=[Point(i, 3) for i in range(2, 5)]
        )

    def test_move(self):
        # Test moving the snake
        self.snake.move()
        self.assertEqual(
            self.snake.points, [Point(i, 3) for i in range(3, 6)]
        )

    def test_set_facing(self):
        # Test setting a direction and moving
        self.snake.set_direction(UP)
        self.assertEqual(self.snake.facing, UP)
        self.snake.move()
        # Remember in curses: -ve y direction is up on the screen
        self.assertEqual(
            self.snake.points,
            [Point(3, 3), Point(4, 3), Point(4, 2)])

    def test_move_blocked_direction(self):
        # Test an attempt to set a direction against the direction of travel
        self.snake.set_direction(LEFT)
        self.assertEqual(self.snake.facing, RIGHT)

    def test_intersect(self):
        self.assertTrue(self.snake.intersect([Point(3, 3)]))
        self.assertFalse(self.snake.intersect([Point(2, 2)]))

    def test_grow(self):
        self.snake.grow_next_turn()
        self.snake.move()
        self.assertEqual(
            self.snake.points,
            [Point(i, 3) for i in range(2, 6)]
        )
        # Move another step and check we still have 4 points
        self.snake.move()
        self.assertEqual(
            self.snake.points,
            [Point(i, 3) for i in range(3, 7)]
        )

    def test_lose_tail(self):
        self.snake.lose_tail()
        self.assertEqual(
            self.snake.points,
            [Point(i, 3) for i in range(3, 5)]
        )

    def test_bad_input(self):
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            Snake(
                name='testsnake',
                start_points=[Point(3, 3), Point(4, 3), Point(4, 4),
                              Point(4, 3), Point(3, 3)]
            )
        with self.assertRaisesRegex(ValueError, 'Broken'):
            Snake(
                name='testsnake',
                start_points=[Point(3, 3), Point(4, 4), Point(4, 3)]
            )
