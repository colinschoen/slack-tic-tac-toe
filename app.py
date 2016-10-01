from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import utils

API_VERSION = 'v1'
STARTING_BOARD = [[None, None, None], [None, None, None], [None, None, None]]

app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config.cfg')
app.config['API_VERSION'] = API_VERSION
app.config['STARTING_BOARD'] = STARTING_BOARD

class Hook(Resource):
    def post(self):
        text = request.form['text']
        return jsonify("""
               {
                    'response_type': 'in_channel'
                    'text': {}
               } 
                """.format(text))

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



if __name__ == "__main__":
    api.add_resource(Hook, '/{}/hook'.format(API_VERSION))
    app.run(host='0.0.0.0')
