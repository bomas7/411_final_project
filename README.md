# 411_final_project
## Bad Weather Checker App 
### Overview
This project is a web-based application designed to do the most important part of weather checking: checking for bad weather! We allow users to set their location to any city in the world and check for the most important part of weather checking: bad weather. We let users know if any days are rain, snow, thunder, or cloudy in the near future.
### To run
  - Obtain an openweather API key and plug that into .env
  - Unit tests:
    - Make sure dependencies in requirements.txt are installed, make sure pytest is installed
    - Run ```python3 -m pytest <path_to_test>```
  - Smoke Tests:
    - Make sure docker is installed
    - Run ```docker-compose up``` within bad_weather_project directory
    - Run ```<path_to_smoketests.sh>```
### Routes 
1. **Set Location**
  - Route Path : `/api/set-location`
  - Request Type  : PUT
  -  Purpose  : Allows users to get change the location (initially set to Boston)
  -  Request Format:
    - city_name (string): Name of city
    - state_code (string): *(Parameter is Only for cities in US)* Name of state
    - country_code (string): ISO 3166 Code of Country of City
  -  Response Format: JSON
  -  Success Response Example:
    - Code: 200
    - Content: { "lon": "30", "lat": "35"}
  -  Example Request: 
    {
      "city_name": "London",
      "country_code": "GB"
    }
  - Example Response:
  {
    "status": 200,
    "data": { "lon": "30", "lat": "35"}
  }

2. **Set Custom Location**
  - Route: `/api/bad-weather-checker`  
  - Request Type : `GET`  
  - Purpose : Check if the main weather over next five days is bad and return a list of weather status corresponding to each day
  - Request Format: JSON
  - Response Format : JSON    
  -  Success Response Example:
        - Code: 200
        - Content: { "weather": ['Cloudy', 'Rain', 'Thunderstorm', 'Snow', 'None']}
  - Example Request: 
      {}
  - Example Response:
    {
      "status": 200,
      "weather": "['Cloudy', 'Rain', 'Thunderstorm', 'Snow', 'None']
    }
    
## REPLACE THESE WITH ALL OTHER ROUTES ##
 3. **Bad Weather Forecast**
  - Route Name and Path: `/precipitation`  
  - Request Type: `GET`  
  - Purpose : Get five day weather forecast based on set location (gives Boston location if none is set).  
  - Request Format: Boston
  - Request Format JSON
  - Request Body: N/A
  - Response Format: JSON
    Success Response Example:
      - Code: 200
      - Content: { "weather": ["none", "rain", "thunderstorm"] }
  - Example Request: {}
  - Example Response: 
    {
      "status": "200",
      "data": {"weather": ["none", "rain", "thunderstorm"]}
    }
    
    
4. **Login**
  - Route Name and Path: `/login`  
  - Request Type: `POST`  
  - Purpose : Login to user account with username and password and verifies based on hashed password
  - Request Format JSON
  - Request Body: 
    - username (string): User's username
    - password (string): User's password
  - Response Format: JSON
    Success Response Example:
      - Code: 200
      - Content: { "message": "logged in" }
  - Example Request: 
  {
    "username": "test",
    "password": "securepassword",
  }
  - Example Response: 
    {
      "status": "200",
      "message": "logged in"
    }


5. **Create Account**
  - Route Name and Path: `/create_account`  
  - Request Type: `POST`  
  - Purpose : Create a new user account with associated username and password
  - Request Format JSON
  - Request Body: 
    - username (string): User's username
    - password (string): User's password
  - Response Format: JSON
    Success Response Example:
      - Code: 200
      - Content: { "message": "account created" }
  - Example Request: 
  {
    "username": "test",
    "password": "securepassword",
  }
  - Example Response: 
    {
      "status": "200",
      "message": "account created"
    }

6. **Update-Password**
  - Route Name and Path: `/updated_password`  
  - Request Type: `PUT`  
  - Purpose : Update user's password with new password
  - Request Format JSON
  - Request Body: 
    - username (string): User's username
    - new_password (string): User's new_password
  - Response Format: JSON
    Success Response Example:
      - Code: 200
      - Content: { "message": "account created" }
  - Example Request: 
  {
    "username": "test",
    "password": "securepassword",
  }
  - Example Response: 
    {
      "status": "200",
      "message": "new password set"
    }
