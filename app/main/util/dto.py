from flask_restplus import Namespace, fields

class SampleDto:
    api = Namespace('Sample', description='Sample API')

class AssembleDto:
    api = Namespace('Assembly Operations', description='Scenario assembly endpoints')
    assemblyinput = api.model('input', {
        'flow_id': fields.String(required=True, description='Parent workflow identifier'),
        'n_model_id': fields.String(required=True, description='Identifier of the model to prepare assembly for'),
        'm_dependency_ids' : fields.List(fields.String(required=False), description='List of model dependency identifiers')
    })

