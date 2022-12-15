from flask import request
from flask_restplus import Resource
from ..util.dto import AssembleDto
from ..service.assemble_service import simple_assembly, full_assembly

api = AssembleDto.api
_assemblyinput = AssembleDto.assemblyinput

@api.route('/<flow_id>/<model_id>')
@api.param('model_id', 'Identifer of target model for assembly')
@api.param('flow_id', 'Identifier of parent workflow')
class SimpleAssembly(Resource):
    @api.doc('Perform a simple assembly operation with no model dependencies', security=None)
    @api.response(200, 'The request was received succesfully')
    @api.response(500, 'Internal error occured')
    def get(self, flow_id, model_id):
        """Perform a simple assembly operation with no model dependencies"""
        # TODO: Sanitize and validate inputs (alphanumeric and dash)
        # Call service simple assemble
        response = simple_assembly(flow_id, model_id)
        return response

@api.route('/')
class FullAssembly(Resource):
    @api.doc('Perform a complex assembly operation with model dependencies', security=None)
    @api.response(200, 'The request was received succesfully')
    @api.response(500, 'Internal error occured')
    @api.expect(_assemblyinput, validate=True)
    def post(self):
        """Perform a complex assembly operation with model dependencies"""
        data = request.json
        # response = complex_assembly(flow_id, model_id, data)
        response = full_assembly(data)
        return response
