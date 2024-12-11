import logging
import os
import time
from typing import Any, List
import requests

# from dotenv import load_dotenv
# load_dotenv()

from bad_weather_checker.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


API_KEY = os.getenv("WEATHER_API_KEY")

DEFAULT_CITY = "Boston"
DEFAULT_STATE = "Massachusetts"
DEFAULT_COUNTRY = "US"

class WeatherModel:
    """
    A class to manage bad weather checking.

    Attributes:
        city_name (str): Name of city to check weather of
        state_code (str): State code of city to check weather of (FIPS code)
        country_code (str): Country code of city to check weather of (ISO 3166 code)
    """

    def __init__(self):
        """Initializes the weather model with default location"""
        self.city: str = DEFAULT_CITY
        self.state: str = DEFAULT_STATE
        self.country: str = DEFAULT_COUNTRY

    def get_coordinates(self) -> dict[str, str]:
        """
        Gets latitude and longitude coordinates
        Returns:
            dict[str, str]: A dictionary containing the latitude and longitude coordinates, empty if error
        """
        request_url = f"http://api.openweathermap.org/geo/1.0/direct"
        q_str = ""
        if self.state == "":
            q_str = f"{self.city},{self.country}"
        else:
            q_str = f"{self.city},{self.state},{self.country}"
        params = {
            "q": q_str,
            "appid": API_KEY
        }
        logger.info("Requesting coordinates of location")
        response = requests.get(request_url, params)
        try:
            if response.status_code == 200:
                data = response.json()
                lat = data[0]['lat']
                lon = data[0]['lon']
                logger.info("Successfully retrieved coordinates of location")
                return {"lat": lat, "lon": lon}
        except:
            logger.error("Could not retrieve coordinates of location")
        return {}

    def set_location(self, city, country, state="") -> bool:
        """
        Sets custom location if valid
        Parameters:
            city (str): name of city
            country (str): name of country
            state (str, optional): name of state if city part of United States
        Returns:
            bool: whether or not location was set to requested place
        """
        old_city = self.city
        old_state = self.state
        old_country = self.country
        self.city = city
        self.country = country
        self.state = state
        logger.info("Checking if custom location is valid")
        coordinates = self.get_coordinates()
        print(coordinates)
        if coordinates == {}:
            logger.error("Not valid custom coordinates, restoring old parameters")
            self.city = old_city
            self.state = old_state
            self.country = old_country
            return False
        else:
            logger.info("Keeping custom coordinates, confirmed valid")
            return True

    def bad_weather_checker(self) -> List[str]:
        """
        Checks the main weather over next 5 days and lists bad weather (none if good weather) for each day
        Returns:
            List[str]: a list of weather conditions over the next 5 days
        """
        request_url = "http://api.openweathermap.org/data/2.5/forecast?"
        logger.info("Requesting Bad Weather Checks")
        coordinates = self.get_coordinates()
        if 'lat' not in coordinates or 'lon' not in coordinates:
            raise ValueError("Location is no longer valid")
        lat = coordinates['lat']
        lon = coordinates['lon']
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        }
        response = requests.get(request_url, params)
        try:
            if response.status_code == 200:
                logger.info("Successfully got bad weather data")
                data = response.json()
                res = []
                for i in data['list'][:5]:
                    weather = i['weather'][0]['main']
                    # print(weather)
                    if weather == 'Rain':
                        res.append("Rain")
                    elif weather == 'Thunderstorm':
                        res.append("Thunderstorm")
                    elif weather == 'Snow':
                        res.append("Snow")
                    elif weather == 'Clouds':
                        res.append("Clouds")
                    else:
                        res.append("None")
                    # res.append(weather)
                return res
        except:
            logger.error("Could not retrieve bad weather data")
        return []

# test = WeatherModel()
# print(test.bad_weather_checker())
# print(test.get_coordinates())
# print(test.set_location("this should be none", "lol"))
# print(test.set_location("London", "GB"))
# print(test.bad_weather_checker())
# print(test.set_location("Ontario", "CA"))
# print(test.bad_weather_checker())