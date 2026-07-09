import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gps_data import calculate_distance


class TestHaversine(unittest.TestCase):
    def test_same_point_is_zero(self):
        self.assertEqual(calculate_distance(47.2, 11.4, 47.2, 11.4), 0.0)

    def test_one_degree_longitude_at_equator(self):
        distance = calculate_distance(0.0, 0.0, 0.0, 1.0)
        self.assertAlmostEqual(distance, 111195, delta=50)

    def test_symmetry(self):
        forward = calculate_distance(47.2, 11.4, 47.3, 11.5)
        backward = calculate_distance(47.3, 11.5, 47.2, 11.4)
        self.assertAlmostEqual(forward, backward, places=6)

    def test_known_distance_positive(self):
        distance = calculate_distance(47.2, 11.4, 47.3, 11.4)
        self.assertGreater(distance, 0)


if __name__ == "__main__":
    unittest.main()