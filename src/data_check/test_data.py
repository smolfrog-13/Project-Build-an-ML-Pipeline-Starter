import pandas as pd
import numpy as np
import pytest
from scipy.stats import ks_2samp

########################################################
# Existing tests (DO NOT MODIFY)
########################################################

def test_column_names(data):
    expected_columns = [
        "id",
        "name",
        "host_id",
        "host_name",
        "neighbourhood_group",
        "neighbourhood",
        "latitude",
        "longitude",
        "room_type",
        "price",
        "minimum_nights",
        "number_of_reviews",
        "last_review",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
    ]
    assert list(data.columns) == expected_columns


def test_neighborhood_names(data):
    neighborhoods = data["neighbourhood_group"].unique()
    expected = {
        "Manhattan",
        "Brooklyn",
        "Queens",
        "Bronx",
        "Staten Island",
    }
    assert set(neighborhoods) == expected


def test_proper_boundaries(data):
    idx = data["longitude"].between(-74.25, -73.50)
    idx &= data["latitude"].between(40.5, 41.2)
    assert idx.all()


def test_similar_neigh_distrib(data, ref_data, kl_threshold):
    for neigh in data["neighbourhood_group"].unique():
        dist_data = data[data["neighbourhood_group"] == neigh]["price"]
        dist_ref = ref_data[ref_data["neighbourhood_group"] == neigh]["price"]
        _, p_value = ks_2samp(dist_data, dist_ref)
        assert p_value > kl_threshold


########################################################
# Implement here test_row_count and test_price_range   #
########################################################

def test_row_count(data):
    assert 15000 < data.shape[0] < 1000000


def test_price_range(data, min_price, max_price):
    assert data["price"].between(min_price, max_price).all()
