#coding: utf-8

from flask import Flask
from flask_restful import Api, Resource
from webargs import fields
from webargs.flaskparser import use_args
import engine

app = Flask(__name__)
api = Api(app)

class Distance(Resource):

    coordinates = {
    'x1': fields.Float(missing=0.0),
    'y1': fields.Float(missing=0.0),
    'x2': fields.Float(missing=0.0),
    'y2': fields.Float(missing=0.0)
    }

    @use_args(coordinates)
    def get(self, args):
        distance = engine.get_distance(args['x1'], args['y1'], args['x2'], args['y2'])
        return {"distance": distance}

api.add_resource(Distance, "/distance")

if __name__ == '__main__':
    app.run(debug=True)
