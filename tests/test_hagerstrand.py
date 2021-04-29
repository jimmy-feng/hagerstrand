#!/usr/bin/env python

"""Tests for `hagerstrand` package."""

import os
import unittest
import geopandas as gpd
from hagerstrand import hagerstrand, dataprocess


class TestHagerstrand(unittest.TestCase):
    """Tests for `hagerstrand` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        print("setUp")
        self.in_shp = os.path.abspath("examples/data/KnoxCountyBlockGroup.shp")
        self.in_gmapjson = os.path.abspath("examples/data/LocationHistory.json")
        self.in_csv = os.path.abspath("examples/data/core_poi-geometry-patterns-sgpid.csv")

    def tearDown(self):
        """Tear down test fixtures, if any."""
        print("tearDown\n")

    def test_shp_to_geojson(self):
        print("test_shp_to_geojson")
        self.assertIsInstance(hagerstrand.shp_to_geojson(self.in_shp), dict)
    
    def test_gmapjson_to_geojson(self):
        print("test_gmapjson_to_geojson")
        self.assertIsInstance(hagerstrand.gmapjson_to_geojson(self.in_gmapjson), dict)

    def test_poly_centroid(self):
        print("test_poly_centroid")
        self.assertIsInstance(hagerstrand.poly_centroid(self.in_shp, 6576, True, 4326), gpd.GeoDataFrame)

    def test_csv_to_gdf(self):
        print("test_csv_to_gdf")
        self.assertIsInstance(hagerstrand.csv_to_gdf(in_csv=self.in_csv, index_col=0), gpd.GeoDataFrame)


if __name__ == '__main__':
    unittest.main()
