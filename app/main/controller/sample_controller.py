from flask import request
from flask_restplus import Resource
from ..util.dto import SampleDto
from flask_jwt import jwt_required

api = SampleDto.api

@api.route('')
class Recommender(Resource):
    @api.doc('sample endpoint with no security', security=None)
    @api.response(200, 'The request was received succesfully')
    @api.response(500, 'Internal error occured')
    def get(self):
        """Returns hello world with no security"""
        return "Hello World!!! No Security Here"

    @api.doc('sample endpoint with security')
    @jwt_required()
    @api.response(200, 'The request was received succesfully')
    @api.response(500, 'Internal error occured')
    def put(self):
        """Returns hello world with security"""
        return "You have the power!!!"
    