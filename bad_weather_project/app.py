from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized
# from flask_cors import CORS

from config import ProductionConfig, TestConfig
from bad_weather_checker.db import db
from bad_weather_checker.models.mongo_session_model import login_user, logout_user
from bad_weather_checker.models.user_model import Users
from bad_weather_checker.models.weather_model import WeatherModel

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables
    weather_model = WeatherModel()
    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """
        Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.
        """
        app.logger.info('Health check')
        return make_response(jsonify({'status': 'healthy'}), 200)

    @app.route('/api/create-user', methods=['POST'])
    def create_user() -> Response:
        """
        Route to create a new user.

        Expected JSON Input:
            - username (str): The username for the new user.
            - password (str): The password for the new user.

        Returns:
            JSON response indicating the success of user creation.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue adding the user to the database.
        """
        app.logger.info('Creating new user')
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Extract and validate required fields
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)

            # Call the User function to add the user to the database
            app.logger.info('Adding user: %s', username)
            Users.create_user(username, password)

            app.logger.info("User added: %s", username)
            return make_response(jsonify({'status': 'user added', 'username': username}), 201)
        except Exception as e:
            app.logger.error("Failed to add user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/login', methods=['POST'])
    def login():
        """
        Route to log in a user

        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The user's password.

        Returns:
            JSON response indicating the success of the login.

        Raises:
            400 error if input validation fails.
            401 error if authentication fails (invalid username or password).
            500 error for any unexpected server-side issues.
        """
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            app.logger.error("Invalid request payload for login.")
            raise BadRequest("Invalid request payload. 'username' and 'password' are required.")

        username = data['username']
        password = data['password']
        # print(username)
        # print(password)

        try:
            # Validate user credentials
            if not Users.check_password(username, password):
                app.logger.warning("Login failed for username: %s", username)
                raise Unauthorized("Invalid username or password.")

            # Get user ID
            user_id = Users.get_id_by_username(username)

            # Load user's combatants into the battle model
            #login_user(user_id, battle_model)

            app.logger.info("User %s logged in successfully.", username)
            return jsonify({"message": f"User {username} logged in successfully."}), 200

        except Unauthorized as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            app.logger.error("Error during login for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500

    @app.route('/api/update-password', methods=['PUT'])
    def update_password():
        """
        Route to update password

        Expected JSON Input:
            - username (str): The username of the user.
            - new_password (str): The user's new_password.

        Returns:
            JSON response indicating the success of the login.

        Raises:
            500 error if any issues
        """
        try:
            data = request.get_json()
            if not data or 'username' not in data or 'new_password' not in data:
                app.logger.error("Invalid request payload for password change.")
                raise BadRequest("Invalid request payload. 'username' and 'password' are required.")

            username = data['username']
            new_password = data['new_password']
            Users.update_password(username, new_password)

            app.logger.info("User %s successfully changed password", username)
            return jsonify({"message": "Successfully changed password"}), 200

        except Exception as e:
            app.logger.error("Error during password change %s", str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500

    @app.route('/api/logout', methods=['POST'])
    def logout():
        """
        Route to log out a user and save their combatants to MongoDB.

        Expected JSON Input:
            - username (str): The username of the user.

        Returns:
            JSON response indicating the success of the logout.

        Raises:
            400 error if input validation fails or user is not found in MongoDB.
            500 error for any unexpected server-side issues.
        """
        data = request.get_json()
        if not data or 'username' not in data:
            app.logger.error("Invalid request payload for logout.")
            raise BadRequest("Invalid request payload. 'username' is required.")

        username = data['username']

        try:
            # Get user ID
            user_id = Users.get_id_by_username(username)

            # Save user's combatants and clear the battle model
            #logout_user(user_id, battle_model)

            app.logger.info("User %s logged out successfully.", username)
            return jsonify({"message": f"User {username} logged out successfully."}), 200

        except ValueError as e:
            app.logger.warning("Logout failed for username %s: %s", username, str(e))
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            app.logger.error("Error during logout for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500


    @app.route('/api/init-db', methods=['POST'])
    def init_db():
        """
        Initialize or recreate database tables.

        This route initializes the database tables defined in the SQLAlchemy models.
        If the tables already exist, they are dropped and recreated to ensure a clean
        slate. Use this with caution as all existing data will be deleted.

        Returns:
            Response: A JSON response indicating the success or failure of the operation.

        Logs:
            Logs the status of the database initialization process.
        """
        try:
            with app.app_context():
                app.logger.info("Dropping all existing tables.")
                db.drop_all()  # Drop all existing tables
                app.logger.info("Creating all tables from models.")
                db.create_all()  # Recreate all tables
            app.logger.info("Database initialized successfully.")
            return jsonify({"status": "success", "message": "Database initialized successfully."}), 200
        except Exception as e:
            app.logger.error("Failed to initialize database: %s", str(e))
            return jsonify({"status": "error", "message": "Failed to initialize database."}), 500

    @app.route('/api/set-location', methods=['PUT'])
    def set_location():
        """
        Route to set a location

        Expected JSON Input:
            - city (str): The name of the city to be set.
            - country (str): The country of the city to be set.
            - state (str, optional): If in the United States, the state of the city to be set.

        Returns:
            JSON response indicating the success of setting custom location
        Raises:
            400 error if input validation fails.
            500 error if there is an issue adding the user to the database.   
        """
        app.logger.info("Attempting to set-location")
        try:
            data = request.get_json()
            if not data or 'city' not in data or 'country' not in data:
                app.logger.error("Invalid request payload for set-location.")
                raise BadRequest("Invalid request payload.")
            works = False
            if 'state' not in data:
                works = weather_model.set_location(data['city'], data['country'])
            else:
                works = weather_model.set_location(data['city'], data['country'], data['state'])
            if not works:
                raise ValueError("Invalid Exception")
            return jsonify({"message": f"Location set successfully"}), 200
        except ValueError as e:
            app.logger.error("Invalid location during setlocation %s", str(e))
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            app.logger.error("Error during setlocation %s", str(e))
            return jsonify({"error": str(e)}), 500

    @app.route('/api/bad-weather-checker', methods=['GET'])
    def bad_weather_checker():
        """
        Route to check for bad weather

        Returns:
            JSON response indicating the success of user creation.
        Raises:
            500 error if there is an issue with getting bad weather
        """
        app.logger.info("Attempting to retrieve bad weather checking for location.")
        try:
            res = weather_model.bad_weather_checker()
            if not res:
                app.logger.error("Could not retrieve anything in bad weather checker")
                raise ValueError("Location no longer valid/Error retrieving")
            app.logger.info("Successfully got bad weather")
            return jsonify({"data": res}), 200
        except Exception as e:
            app.logger.error("Error during bad-weather-checker %s", str(e))
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)