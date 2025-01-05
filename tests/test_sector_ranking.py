import unittest
from unittest.mock import patch

from recommendation_service.sector_ranking import SectorRanking


class TestSectorRanking(unittest.TestCase):
    def setUp(self):
        self.sector_ranking = SectorRanking()

    def test_init(self):
        self.assertIsNone(self.sector_ranking.industries)
        self.assertIsNone(self.sector_ranking.prices_1y)
        self.assertIsNone(self.sector_ranking.vnindex_1y)
        self.assertIsNone(self.sector_ranking.ranked_sectors)


if __name__ == "__main__":
    unittest.main()
