#Import the flask modules
import os
from flask import Flask, request, jsonify, render_template, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
 
#Create a Flask constructor
app = Flask(__name__, template_folder='swagger/templates')

# Including config file
app.config.from_object("config.Config")

# This variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# This variable, ma, will be used for all Marshmallow commands
ma = Marshmallow(app)

from .models import Game, GameSchema

# APISpec object with basic API informations.
spec = APISpec(
    title="Video Game Suggestion API Doc",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="API endpoints to get combination of games that has the highest total value of all possible game combinations that fits given pen-drive space"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# OpenAPI docs endpoint
@app.route('/api/swagger.json')
def create_swagger_json():
    return jsonify(spec.to_dict())

# /api/v1/status endpoint to check  database health status.
@app.route("/api/v1/status", methods=['GET', 'HEAD'])
def check_db_health_get():
    """Get Database health status
    ---
    get:
        description: Get Database health status
        responses:
            200:
                description: Returns database connection is healthy
            503:
                description: Returns database connection is unhealthy
                 
    """
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        if request.method == 'GET':
            return jsonify({"database" : "healthy"}), 200
        else:
            response = Response()
            response.headers["status-code"] = "200"
            return response
    except Exception as e:
        if request.method == 'GET':
            return jsonify({"database" : "unhealthy"}), 503
        else:
            response = Response()
            response.headers["status-code"] = "503"
            return response

# /api/v1/games endpoint to create game.
@app.route('/api/v1/games', methods=['POST'])
def create_game():
    """Create Game
    ---
    post:
        description: Validates and stores game
        requestBody:
            required: true
            content:
                application/json:
                    schema: GameSchema
        responses:
            201:
                description: Returns game object.
                content:
                    application/json:
                        schema: GameSchema
            400:
                description: Returns validation error messages.
            409:
                description: Game name already exists error.
                 
    """
    data  = request.get_json()

    try:
        # validate and store game data
        GameSchema().load(data)
        game = Game(name=data['name'], price=data['price'], space=data['space'])
        db.session.add(game)
        db.session.commit()

        # serialize the game data
        schema = GameSchema(only=("name", "price", "space"))
        result = schema.dump(game)

        return jsonify({"message" : "success", "data" : result}), 201

    except ValidationError as err:
        return jsonify({"message" : err.messages}), 400

    except KeyError as err:
        return jsonify( {
                        "message": {
                            err.args[0]: [
                                "Key is missing."
                            ]
                        }
                    }), 400

    except IntegrityError:
        app.logger.error(IntegrityError)
        return jsonify({"message" : 'Game name already exists'}), 409

# /api/v1/best_value_games endpoint to fetch a combination of games that has the highest total value of all possible game combinations 
#  that fits given pen-drive space
@app.route('/api/v1/best_value_games', methods=['POST'])
def best_value_games():
    """Get combination of games that fits given pendrive space
    ---
    post:
        description: Fetch a combination of games that has the highest total value of all possible game combinations that fits given pen-drive space
        parameters:
          - in: query
            name: pen_drive_space
            schema:
              type: integer
            description: The pendrive space value.
        responses:
            201:
                description: Returns combination of games that fits given pen-drive space parameters.
                content:
                    application/json:
                        schema: GameSchema
            400:
                description: Returns pendrive space validation error messages.
                 
    """
    pen_drive_space = request.args.get('pen_drive_space', default=0, type=int)

    # Validating the value of pen drive is greater than 0
    if pen_drive_space < 0:
        return jsonify({"message" : "Pen-drive space value should be a greater than 0."}), 400
    
    # Validating the value of pen drive is not null
    if pen_drive_space == None or pen_drive_space == '' or pen_drive_space == 0:
        return jsonify({"message" : "Pen-drive space value(in bytes) is required"}), 400
    
    # Get all the games that are less than the total space of the pen drive.
    games = Game.query.filter(Game.space < pen_drive_space).order_by(Game.space.desc()).all()
    total_game_size = 0
    total_price = 0
    remaining_space = pen_drive_space
    games_array = []
    
    # Identifying the combination of games that has the highest total value of all possible game combinations 
    #  that fits given pen-drive space
    try:
        for game in games:
            if(int(total_game_size+game.space) <= int(pen_drive_space)):
                total_game_size += game.space
                total_price += game.price
                remaining_space = int(pen_drive_space-total_game_size)
                schema = GameSchema(only=("name", "price", "space"))
                result = schema.dump(game)
                games_array.append(result)

        return jsonify({
                            "games" : games_array, 
                            "total_space" : total_game_size, 
                            "remaining_space" : remaining_space, 
                            "total_value": total_price
                        }), 201
    except Exception as e:
        app.logger.error("Endpoint : /api/v1/best_value_games, error : %s" %e)
        return jsonify({"message" : "Something went wrong !!"}), 400

# Since apispec path inspects the view and its route,
# we need to be in a Flask request context    
with app.test_request_context():
    spec.path(view=check_db_health_get)
    spec.path(view=create_game)
    spec.path(view=best_value_games)

# swagger-ui routes
@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', path)

#Create the main driver function
if __name__ == '__main__':
#call the run method
    app.run(debug=os.getenv("FLASK_DEBUG"),host=os.getenv("FLASK_HOST"))