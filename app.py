from flask import Flask, jsonify
from flask_restful import Resource, Api
import utils

API_VERSION = 'v1'
STARTING_BOARD = [[None, None, None], [None, None, None], [None, None, None]]

app = Flask(__name__)
api = Api(app)

class Board(Resource):
    def get(self):
        return utils.getBoard([[None, 0, 1], [None, 0, 0], [None, None, 0]])

api.add_resource(Board, '/{}/board'.format(app.config['API_VERSION']))

if __name__ == "__main__":
    app.config.from_pyfile('config.cfg')
    app.config['API_VERSION'] = API_VERSION
    app.config['STARTING_BOARD'] = STARTING_BOARD
    app.run(host='0.0.0.0')
