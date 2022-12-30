"""Tests for Location Model"""
import pytest
from app.database.models.location import Location, LocationProviders


def test_aws_provider():
    provider = LocationProviders["AWS"]
    assert provider == LocationProviders.AWS


def test_bb_provider():
    provider = LocationProviders["BB"]
    assert provider == LocationProviders.BB


def test_do_provider():
    provider = LocationProviders["DO"]
    assert provider == LocationProviders.DO


def test_missing_provider():
    with pytest.raises(ValueError):
        Location.from_dict({
            "region": "FRA1",
            "file_path": "cdn/file/test.png"
        })


def test_missing_path():
    with pytest.raises(ValueError):
        Location.from_dict({
            "region": "FRA1",
            "provider": "AWS"
        })


def test_missing_region():
    with pytest.raises(ValueError):
        Location.from_dict({
            "file_path": "cdn/file/test.png",
            "provider": "AWS"
        })
