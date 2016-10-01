from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import utils

API_VERSION = 'v1'
STARTING_BOARD = [[None, None, None], [None, None, None], [None, None, None]]

app = Flask(__name__)
api = Api(app)

class Hook(Resource):
    def post(self):
        text = request.form['text']
        return jsonify(text)

def start_game(channel, player0, player1):
    """
    Starts a new game in channel if one does not exist already
    
    Args:
        channel(str): The Slack CID to start the game in
        player0(str): The Slack UID of the first player in the game
        player1(str): The Slack UID of the second player in the game
        
    Returns:
        None
    """
    pass

api.add_resource(Hook, '/{}/hook'.format(app.config['API_VERSION']))

if __name__ == "__main__":
    app.config.from_pyfile('config.cfg')
    app.config['API_VERSION'] = API_VERSION
    app.config['STARTING_BOARD'] = STARTING_BOARD
    app.run(host='0.0.0.0')
