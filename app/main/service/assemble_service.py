import os
import json
from flask import json as flask_json
from flask import Response
from ..model.base_scenario import BaseScenario
from ..model.model_parameter import ModelParameter
from ..model.model_set import ModelSet
from ..model.model_output import ModelOutput
from ..model.flowmap import FlowMap
# from mongoengine import connect, disconnect_all
from app.main.config import config_by_name
from ..handler.specification_handler import SpecificationHandler

def full_assembly(data):
    """
    Decide what type of assembly method to use.
    """
    # TODO: Add try catch

    try:

        flow_id = data['flow_id']
        model_id = data['n_model_id']

        if ( not flow_id or not model_id):
            raise Exception("Invalid flow or model ids")
        
        if ('m_dependency_ids' in data):
            dependencies = data['m_dependency_ids']
            return complex_assembly(flow_id, model_id, dependencies)
    
        return simple_assembly(flow_id, model_id)
    
    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500  


def simple_assembly(flow_id, model_id):
    """
    Assemble a SWIM scenario specification with no model dependencies.
    """

    try:

        sh = SpecificationHandler(flow_id, model_id)
        scenario_spec = sh.simple_assemble()

        # export to file (testing only)
        # sh.export_json('simple_assembly.json')
        
        sh.save_run()
        sh.disconnect_db()

        # prepare scenario spec for endpoint response
        resp = Response(flask_json.dumps(scenario_spec.__dict__),
                    mimetype='application/json')

        return resp

    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500  

def complex_assembly(flow_id, model_id, dependencies):
    """
    Assemble a SWIM scenario specification with model dependencies.
    """
    try:

        sh = SpecificationHandler(flow_id, model_id)
        scenario_spec = sh.complex_assemble(dependencies)

        # export to file (testing only)
        #sh.export_json('complex_assembly.json')

        # save run to database
        sh.save_run()

        # disconnect db
        sh.disconnect_db()

        # prepare scenario spec for endpoint response
        resp = Response(flask_json.dumps(scenario_spec.__dict__),
                    mimetype='application/json')

        return resp

    except Exception as e:
        response = {
            'status': 'fail',
            'message': str(e)
        }
        return response, 500 
