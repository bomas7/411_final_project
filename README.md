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
  - Route Path : `/api/bad-weather-checker`  
  - Request Type : `GET`  
  - Purpose : Check if the main weather over next five days is bad and return a list of weather status corresponding to each day
  - Request Format: JSON
  - Response Format: JSON    
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
    
  3. **Create User**
  - Route Path : `/api/create-user`
  - Request Type : `POST`
  - Purpose : Allows users to create a new user account.
  - Request Format:
  -  username (string): The username for the new user.
  -  password (string): The password for the new user.
  - Response Format: JSON
  - Success Response Example:
      - Code: 201
      - Content: { "username": "example_username" }
  - Example Request:
   { 
     "username": "weatherman",
     "password": "password"
   }
  - Example Response:
  {
    "status": 201,
    "username": "weatherman"
  } 

4. **User Login**
- Route Path : `/api/login`
- Request Type  : POST
- Purpose  : Authenticate a user and allow them to log in.
- Request Format:
    - username (string): The username of the user.
    - password (string): The user's password.
- Response Format: JSON
- Success Response Example:
    - Code: 200
    - Content: { "message": "User example_username logged in successfully." }
- Example Request:
{
  "username": "weatherman",
  "password": "password"
}
- Example Response:
{
  "status:: 200
  "message": "User example_username logged in successfully."
}

5. **Update Password**
- Route Path  : `/api/update-password`
- Request Type  : PUT
- Purpose  : Update a user's password.
- Request Format:
    - username (string): The username of the user.
    - new_password (string): The user's new password.
- Response Format: JSON
- Success Response Example:
    - Code: 200
    - Content: { "message": "Successfully changed password" }
- Example Request:
{
  "username": "weatherman",
  "new_password": "newpassword"
}
- Example Response:
{
  "status" 200
  "message": "Successfully changed password"
}

6. **User Logout**
- Route Path  : `/api/logout`
- Request Type  : POST
- Purpose  : Log out a user.
- Request Format:
    - username (string): The username of the user.
    - Response Format: JSON
- Success Response Example:
    - Code: 200
    - Content: { "message": "User weatherman logged out successfully." }
- Example Request:
{
  "username": "weatherman"
}
- Example Response:
{
  "message": "User weatherman logged out successfully."
}

7. **Initialize Database**
- Route Path  : `/api/init-db`
- Request Type  : POST
- Purpose  : Initialize or recreate database tables. Use with caution as this will delete existing data.
- Request Format: None
- Response Format: JSON
- Success Response Example:
    - Code: 200
    - Content: { "message": "Database initialized successfully."
}
- Example Request: {}
- Example Response:
{
    "status": 200,
    "message": "Database initialized successfully."
}
