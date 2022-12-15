import os
import json
import uuid
from flask import json as flask_json
from flask import Response
from app.main.config import config_by_name
from mongoengine import connect, disconnect_all
from ..model.base_scenario import BaseScenario
from ..model.model_parameter import ModelParameter
from ..model.model_set import ModelSet
from ..model.model_output import ModelOutput
from ..model.flowmap import FlowMap
from ..model.runs import Run
from ..model.public_scenario import PublicScenario

class SpecificationHandler:
    
    def __init__(self, flow_id, model_id):

        # verify flow id exists on workflow database
        self.__flow_check(flow_id)

        # TODO: validate that the modelid is part of the flow mappings

        self.flow_id = flow_id
        self.model_id = model_id
        self.dbConnected = False
        self.spec_ready = False

        self.connect_db()
        self.__initialize_spec()

    def save_run(self):
        # TODO:  protect this query for unique flow id and model combination on databse

        Run(_id= str(uuid.uuid4()), runid=self.base_scenario.id, flowid=self.flow_id, modelid=self.model_id).save()

    def simple_assemble(self):
        """
        Assembles a SWIM scenario specification for model execution from a
        workflow. Does not consider other model dependencies.

        Returns:
        SWIM scenario specification as an applicatio/json response.
        """
        print('Processing simple assemble...')

        self.__load_model_parameters()
        self.__load_model_sets()
        self.__load_model_outputs()

        self.base_scenario.status = 'ready'
        self.spec_ready = True

        return self.base_scenario

    def complex_assemble(self, dependencies):
        """
        Assembles a SWIM scenario specification for model execution from a 
        workflow. Takes into account other model dependencies.

        Returns:
        SWIM scenario specification as an applicatio/json response.
        """
        print('Processing complex assemble...')

        self.__load_model_parameters()

        for dependency_id in dependencies:
            userscenario = self.__fetch_scenario(dependency_id)
            self.__load_dependency_data(userscenario, dependency_id)

        self.__load_model_sets()
        self.__load_model_outputs()

        self.base_scenario.status = 'ready'
        self.spec_ready = True

        return self.base_scenario

    def __fetch_scenario(self, dependency_id):
        '''
        Fetch model runs from the dependency 
        '''

        if(not self.dbConnected):
            raise Exception("MongoDB not connected")

        # print(dependency_id)
        run = Run.objects(flowid=self.flow_id, modelid=dependency_id).fields(runid=1).first()
        # print(run.runid)
        userscenario = PublicScenario.objects(_id=run.runid).only('modelOutputs').first()
        return userscenario
    
    def __flow_check(self, flow_id):
        """
        Check if a model id is part of a given workflow.
        """
        print("Verifying flow id...")

    def connect_db(self):
        """
        Retrieve database connection settings and open connections to swim and
        and workflow database instances.
        """
        print("Connecting mongo databases...")

        # get config setings
        environment = (os.getenv('BOILERPLATE_ENV') or 'dev')
        settings = config_by_name[environment]
        swimURL = settings.MODEL_DATABASE_URL
        workflowURL = settings.WORKFLOW_DATABASE_URL
        
        # connect to mongo database instances
        connect(host=swimURL, alias='swim-db-alias')
        connect(host=workflowURL, alias='workflow-db-alias')

        self.dbConnected = True

    def disconnect_db(self):
        """
        Disconnect all database instances.
        """
        print("Disconnecting databases...")
        disconnect_all()
        self.dbConnected = False


    def export_json(self, path):
        """
        Export an assembled scenario specification to a JSON file to a target path.
        """
        print('Exporting to file...')
        if(not self.spec_ready):
            raise Exception("Model scenario specification not generated")        

        # convert spec to json string for file save
        json_spec = json.dumps(self.base_scenario.__dict__, ensure_ascii=False)

        # save scenario spec to file
        with open(path, 'w') as f:
            f.write(json_spec)


    def __initialize_spec(self):
        """
        Instantiates a base SWIM scenario specification with root metadata.
        """
        print('Initializing spec...')
        self.base_scenario = BaseScenario(self.flow_id)

        settings_entry = {
            "modelID" : self.model_id
        }
        self.base_scenario.modelSettings.append(settings_entry)

    def __load_model_parameters(self):
        """
        Loads default and user changed parameter values and appends to the scenario specification.
        """
        print('Loading model parameters...')

        if(not self.dbConnected):
            raise Exception("MongoDB not connected")

        for model_parameter in ModelParameter.objects(modelID=self.model_id).exclude('_id'):
            # replace with user defined values
            for flow_map in FlowMap.objects(flowID=self.flow_id, modelID=self.model_id, swimID = model_parameter.paramName):
                if (flow_map.paramValue != None):
                    model_parameter.paramValue = flow_map.paramValue['paramValue']
                else:
                    model_parameter.paramValue = model_parameter.paramDefaultValue

            raw_json = model_parameter.to_json(use_db_field=False).lstrip("\"").rstrip("\"")
            obj_json = json.loads(raw_json)
            self.base_scenario.modelInputs.append(obj_json)

    def __load_model_sets(self):
        """
        Loads default model sets and appends to the scenario specification (applies only for hydroeconomic model).
        """

        print('Loading model sets...')

        if(not self.dbConnected):
            raise Exception("MongoDB not connected")

        for model_set in ModelSet.objects(modelID=self.model_id).exclude('_id'):
            if (model_set != None):
                raw_json = model_set.to_json(use_db_field=False).lstrip("\"").rstrip("\"")
                obj_json = json.loads(raw_json)
                self.base_scenario.modelSets.append(obj_json)     

    def __load_model_outputs(self):
        """
        Loads default model output metadata which values will be requested to SWIM model.
        """
        print('Loading model outputs...')

        if(not self.dbConnected):
            raise Exception("MongoDB not connected")

        for model_output in ModelOutput.objects(modelID=self.model_id).exclude('_id'):
            raw_json = model_output.to_json(use_db_field=False).lstrip("\"").rstrip("\"")
            obj_json = json.loads(raw_json)
            self.base_scenario.modelOutputs.append(obj_json)

    def __load_dependency_data(self, userscenario, dependency_id):
        """
        Load data that comes from outputs of other models and append to scenario specification.
        """
        print('Loading Dependency Values')

        if(not self.dbConnected):
            raise Exception("MongoDB not connected")


        dCatalogIDS = [] # catalog ids of incoming model outputs
        tCatalogIDS = [] # catalog ids of target model inputs

        # extract incoming model id from settings object

        dModelID = dependency_id
        # print(dModelID)

        # get a list of flowmaps (catalog id) of the incoming model outputs
        for output_map in  FlowMap.objects(flowID=self.flow_id, modelID=dModelID, type = "output").fields(catalogID=1):
            dCatalogIDS.append(output_map.catalogID)

        # get a list of flowmap (catalog id) of the next model inputs
        for input_map in  FlowMap.objects(flowID=self.flow_id, modelID=self.model_id, type = "input").fields(catalogID=1):
            tCatalogIDS.append(input_map.catalogID)
        
        # extract catalog id collisions from both lists
        intersections = set(dCatalogIDS).intersection(tCatalogIDS)

        # raise exception if no intersections are found
        if not intersections:
            raise Exception("No dependency model intersections found.")
       
        # get the output names from the intersections
        for intersection in intersections:
            # print(intersection)
            dFlowMap =  FlowMap.objects(flowID=self.flow_id, modelID=dModelID, catalogID=intersection, type="output").first()
            tFlowMap =  FlowMap.objects(flowID=self.flow_id, modelID=self.model_id, catalogID=intersection, type="input").first()
            varName = dFlowMap.swimID
            paramName = tFlowMap.swimID
            for d_output in userscenario['modelOutputs']:
                if(d_output['varName'] == varName):
                    for param in self.base_scenario.modelInputs:
                        if (param['paramName'] == paramName):
                            # print(param['paramValue']) # before
                            # print('\r\r')
                            param['paramValue'] = d_output['varValue']
                            # print(param['paramValue']) # after

        # function end
    
