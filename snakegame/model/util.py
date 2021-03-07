"""Useful generic functions or constants"""
from dataclasses import dataclass
from itertools import tee


@dataclass
class Point:
    """Class representing a point on the game grid"""
    x: int
    y: int

    def __add__(self, other):
        """Add points like vectors to return a new Point"""
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Sbtract points like vectors to return a new Point"""
        return Point(self.x - other.x, self.y - other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(tuple([self.x, self.y]))


LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
UP = Point(0, -1)
DOWN = Point(0, 1)

chargroups = [['w','a','s','d'], ['i','j','k','l']]


def pairwise(iterable):
    """Returns pairs of values from the input iterator
    e.g. [0,1,2,..] -> (0, 1), (1, 2), ...

    From itertools documentation
    """
    a, b = tee(iterable)
    # Advance the second iterator
    next(b)
    # zip will stop producing output when any iterator is exhausted, so it
    # doesn't matter that b is 'shorter' than a
    return zip(a, b)


