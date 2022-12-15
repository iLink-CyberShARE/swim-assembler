import json
import uuid

class BaseScenario(object):
    
    def __init__(self, flow_id):
        self.id = str(uuid.uuid4())
        self.name = 'Custom workflow scenario {0}'.format(flow_id)
        self.description = 'Automated workflow scenario derived from workflow id {0}'.format(flow_id)
        self.isPublic = True
        self.status = 'Not Assembled'
        self.modelSettings = []
        self.modelSets = []
        self.modelInputs = []
        self.modelOutputs = []
