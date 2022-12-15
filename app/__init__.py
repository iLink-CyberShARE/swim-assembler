from flask_restplus import Api
from flask import Blueprint, url_for

from .main.controller.sample_controller import api as sample_ns
from .main.controller.assemble_controller import api as assemble_ns


blueprint = Blueprint('assembler', __name__, url_prefix='/swim-assembler')

class CustomAPI(Api):
    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)
        This fix will force a relatve url to the specs.json instead of absolute
        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)

authorizations = {
    'Bearer Auth' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Authorization',
        'description': 'Type in the value input box below: Bearer &lt;JWT&gt; where JWT is the token'
    }
}

api = CustomAPI(blueprint,
          title= "SWIM Scenario Assembler",
          version='1.0',
          description='Transformation service to assemble a model scenario specification for SWIM model consumption.',
          doc='/docs/',
          security='Bearer Auth',
          authorizations = authorizations
          )

api.add_namespace(sample_ns, path='/sample')
api.add_namespace(assemble_ns, path='/assemble')


