import logging

from snakegame.model.util import Point, pairwise

log = logging.getLogger(__name__)


class Snake:
    """The main character of Snake: The Game.

    Represents a snake going around a maze and eating food.
    """

    def __init__(self, name, start_points):
        """Create a Snake object.

        Parameters
        ----------
        name: str
            A user friendly name
        start_points: list(tuple(int, int))
            The initial grid positions of the snake, as an ordered list going
            from tail to head.
        """
        # A name to identify this snake
        self.name = name

        # Check that this is a valid initial configuration - no overlaps
        start_check = [(x, y) for x, y in start_points]
        if len(set(start_check)) != len(start_points):
            raise ValueError("Overlapping input points")
        # Check that this is a valid initial configuration - connected
        for point_a, point_b in pairwise(start_points):
            # Check the separation between neighbouring points is 1
            diff = sum([abs(a - b) for a, b in zip(point_a, point_b)])
            if diff != 1:
                raise ValueError('Broken Snake')

        #: Grid points the snake currently occupies
        self.points = [Point(x, y) for x, y in start_points]

        #: Direction of travel
        self.facing = self.points[1] - self.points[0]

        #: Should the snake grow to occupy more space
        self.grow = False

    @property
    def head(self):
        return self.points[-1]

    @property
    def body(self):
        return self.points[1:-1]

    @property
    def tail(self):
        return self.points[0]

    @property
    def blocked_direction(self):
        return self.points[-2] - self.head

    def grow_next_turn(self):
        """Set the grow flag to true"""
        self.grow = True

    def move(self):
        """Move this snake forward a step in the direction it's facing"""
        next_point = self.head + self.facing
        self.points.append(next_point)
        if not self.grow:
            self.points.remove(self.tail)
        self.grow = False

    def set_direction(self, direction):
        """Set the direction for the snake to move next update

        Parameters
        ----------
        direction: tuple
            One of the predefined LEFT, RIGHT, UP, DOWN tuples in util
        """
        if direction == self.blocked_direction:
            return
        self.facing = direction

    def lose_tail(self):
        """Remove this snake's tail!"""
        self.points.remove(self.tail)

    def intersect(self, points):
        """Check if this snake lies on any of the specified points

        Parameters
        ----------
        points: list(Points)
            A list of points to compare against
        """
        intersecting = set(points).intersection(set(self.points))
        return intersecting
