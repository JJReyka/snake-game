import unittest

from snakegame.model.util import Point


class TestPoint(unittest.TestCase):

    def setUp(self):
        self.point_A = Point(4, 5)
        self.point_B = Point(3, 2)

    def test_add(self):
        self.assertEqual(self.point_A + self.point_B, Point(7, 7))

    def test_sub(self):
        self.assertEqual(self.point_A - self.point_B, Point(1, 3))

    def test_iter(self):
        self.assertEqual([i for i in self.point_A], [4, 5])

    def test_dict(self):
        test_dict = {Point(2, 3): 4}
        self.assertEqual(test_dict[Point(2, 3)], 4)
