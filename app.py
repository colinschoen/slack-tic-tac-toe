from flask import Flask, jsonify
from flask_restful import Resource, Api
import utils

SLACK_TOKEN = ""

app = Flask(__name__)
api = Api(app)

class Board(Resource):
    def get(self):
        return utils.getBoard([[None, 0, 1], [None, 0, 0], [None, None])
