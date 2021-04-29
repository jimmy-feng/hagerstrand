#!/usr/bin/env python

"""Tests for `dataprocess` package."""


import unittest
import pandas as pd
from hagerstrand import dataprocess


class TestDataProcess(unittest.TestCase):
    """Tests for `dataprocess` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        print("setUp")
#        self.in_geojson = os.path.abspath("examples/data/stores.geojson")
        self.in_csv = pd.read_csv("examples/data/core_poi-geometry-patterns-sgpid.csv")
        self.in_csv2 = pd.read_csv("examples/data/core_poi-patterns.csv", index_col=0)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        print("tearDown\n")

    def test_unpack_json(self):
        print("test_json_and_merge")
        self.assertIsInstance(dataprocess.unpack_json(self.in_csv), pd.DataFrame)

    def test_unpack_json_and_merge(self):
        print("test_unpack_json_and_merge")
        self.assertIsInstance(dataprocess.unpack_json_and_merge(self.in_csv2), pd.DataFrame)

#    def test_unique_sorted_columns_plus_ALL(self):
#        print("test_unique_sorted_columns_plus_ALL")
#        self.assertIsInstance(dataprocess.unique_sorted_columns_plus_ALL(self.in_shp, 6576, True, 4326), list)



if __name__ == '__main__':
    unittest.main()
