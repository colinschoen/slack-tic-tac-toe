from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from board import Board

import utils

API_VERSION = 'v1'
STARTING_BOARD = [[None, None, None], [None, None, None], [None, None, None]]
VALID_COMMANDS = ['start', 'board', 'move', 'pony']

app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config.cfg')
app.config['API_VERSION'] = API_VERSION
app.config['STARTING_BOARD'] = STARTING_BOARD

class Hook(Resource):
    def post(self):
        data = request.form
        text = data['text'].split()
        if len(text) < 2:
            return """Please specify a command {} and argument/s."""\
                .format(str(VALID_COMMANDS))
        command = text[0] 
        if command not in VALID_COMMANDS:
            return """{} is not a valid command. The valid commands are {}."""\
                .format(str(VALID_COMMANDS))
        args = text[1:]
        # Call our respective board command
        response = getattr(Board, command)(data, args)
        return jsonify({
                    'response_type': 'in_channel',
                    'text': response
               })

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
    app.run(host='0.0.0.0')
