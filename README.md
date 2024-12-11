# 411_final_project
## Bad Weather Checker App 
### Overview
This project is a web-based application designed to do the most important part of weather checking: checking for bad weather! (ADD MORE)
### Routes 
1. **Get Coordinates**
  - Route Path : `/get_coordinates`
  - Request Type  : GET
  -  Purpose  : Allows users to get the Latitude and Longitude coordinates of a city 
  -  Request Format:
    - city_name (string): Name of city
    - state_code (string): *(Parameter is Only for cities in US)* FIPS Code of State of City
    - country_code (string): ISO 3166 Code of Country of City
  -  Response Format: JSON
  -  Success Response Example:
    - Code: 200
    - Content: { "lon": "30", "lat": "35"}
  -  Example Request: 
    {
      "city_name": "Boston",
      "state_code": "25",
      "country_code": "ISO 3166-2:US"
    }
  - Example Response:
  {
    "status": 200,
    "data": { "lon": "30", "lat": "35"}
  }
2. **Set Custom Location**
  - Route: `/location`  
  - Request Type : `POST`  
  - Purpose : Set custom location for future requests (overrides default of Boston) 
  - Request Format: JSON
    - lon (string): Longitude of city
    - lat (string): Latitude of city
  - Response Format : JSON    
  -  Success Response Example:
        - Code: 200
        - Content: { "message": "success"}
  - Example Request: 
      {
        "lon": "30",
        "lat": "25"
      }
  - Example Response:
    {
      "status": 200,
      "message": "success
    }
    
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