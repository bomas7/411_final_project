import time

import pytest

from bad_weather_checker.models.weather_model import WeatherModel


@pytest.fixture
def weather_model():
    """Fixture to provide a new instance of WeatherModel for each test."""
    return WeatherModel()

def test_default_get_coordinates(weather_model):
    """Test that get_coordinates works for the default location with a state"""
    coordinates = weather_model.get_coordinates()
    assert coordinates == {'lat': 42.3554334, 'lon': -71.060511}, "Default get_coordinates invalid"

def test_custom_get_coordinates(weather_model):
    """Test that get_coordinates works for a custom location without a state"""
    weather_model.city = "London"
    weather_model.country = "GB"
    weather_model.state = ""
    coordinates = weather_model.get_coordinates()
    assert coordinates == {'lat': 51.5073219, 'lon': -0.1276474}, "Custom get_coordinates invalid"

def test_invalid_get_coordinates(weather_model):
    """Test that get_coordinates correctly returns empty dict with invalid location"""
    weather_model.city = "JUNK"
    coordinates = weather_model.get_coordinates()
    assert coordinates == {}, "Coordinates should return empty dict"

def test_set_location(weather_model):
    """Test that set_location correctly returns sets a valid location"""
    works = weather_model.set_location("London", "GB")
    assert works and weather_model.city == "London" and weather_model.state == "" and weather_model.country == "GB", "Location successfully set"

def test_invalid_set_location(weather_model):
    """Test that set_location does not set a location if it is invalid"""
    works = weather_model.set_location("JUNK", "GARBAGE", "VALUES")
    assert not works, "Location should not have changed"

def test_bad_weather_checker(weather_model):
    """Test that bad_weather_checker successfully adds five weather values"""
    bad_weathers = weather_model.bad_weather_checker()
    assert len(bad_weathers) == 5, "Should return forecast of first 5 days"

def test_invalid_bad_weather_checker(weather_model):
    """Test that bad_weather_checker does not add weather values"""
    weather_model.city = "JUNK"
    with pytest.raises(ValueError, match="Location is no longer valid"):
        weather_model.bad_weather_checker()
