import logging
import random

from snakegame.model.util import Point


class Game:
    """Represents the game area and objects within"""

    def __init__(self, dimensions=(10, 10), tick_rate=1):
        self.score = {}
        self.snakes = []
        self.food = []
        self.dimension_max = dimensions
        # TODO: Move out of this class
        self.tick_rate = tick_rate

    @property
    def occupied_squares(self):
        """Squares occupied by an item in the game"""
        occupied = []
        for snake in self.snakes:
            occupied.extend(snake.points)
        for food_pos in self.food:
            occupied.append(food_pos)
        return occupied

    @property
    def unoccupied_squares(self):
        """Squares unoccupied by an item in the game"""
        unoccupied = [
            Point(x, y) for x in range(1, self.dimension_max[0])
            for y in range(1, self.dimension_max[1])
            if Point(x, y) not in self.occupied_squares
        ]
        return unoccupied

    def add_snake(self, snake):
        """Add a player/snake character to the game

        Parameters
        ----------
        snake: Snake
            It's a snake

        Raises
        ------
        ValueError
            If the snake would have to be placed on occupied tiles
        """
        intersections = snake.intersect(self.occupied_squares)
        if intersections:
            raise ValueError(
                f"Snake cannot be added, item already occupying squares: "
                f"{', '.join([str(p) for p in intersections])}"
            )
        self.snakes.append(snake)
        self.score[snake] = 0

    def add_food(self, position):
        """Add a food item to the game"""
        self.food.append(position)

    def update(self):
        """Step the game forward, moving player characters and checking for
        collisions"""

        # Move the snakes
        for snake in self.snakes:
            snake.move()

        # Snakes which should be removed this turn
        to_remove = set()

        for snake in self.snakes:
            # Check for collisions with a food tile
            if snake.head in self.food:
                self.food.remove(snake.head)
                self.score[snake] += 1
                snake.grow_next_turn()
                self.add_food(random.choice(self.unoccupied_squares))

            # Check for collisions with a boundary
            if not self.in_bounds(snake.head):
                to_remove.add(snake)

            # Check for collisions with yourself
            if snake.head in snake.body + [snake.tail]:
                to_remove.add(snake)

            # Check for collisions with the other player
            for othersnake in self.snakes[:]:
                if snake == othersnake:
                    continue
                if snake.head in othersnake.body + [othersnake.head]:
                    to_remove.add(snake)
                elif snake.head == othersnake.tail:
                    snake.grow_next_turn()
                    othersnake.lose_tail()

            # Check everyone's still alive
            for snake in self.snakes:
                if len(snake.points) < 2:
                    to_remove.add()

        if to_remove:
            for snake in to_remove:
                self.snakes.remove(snake)

    def quit(self):
        """A kind of roundabout way to quit the game!"""
        self.snakes = []

    def in_bounds(self, pos):
        """Check if a point is in the game boundaries

        Parameters
        ----------
        pos: Point
            A point to be tested
        """
        for p, d_max in zip(pos, self.dimension_max):
            if not 0 < p < d_max:
                return False
        return True



