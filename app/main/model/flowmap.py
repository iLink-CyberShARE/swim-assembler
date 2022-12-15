from mongoengine import *

class FlowMap(Document):
    _id = StringField(primary_key=True)
    className = StringField(required=False)
    flowID = StringField(required=True)
    modelID = StringField(required=True)
    catalogID = StringField(required=True)
    swimID = StringField(required=True)
    type = StringField(required=True)
    paramValue = DynamicField(required=False)
    meta = {
        'collection': 'flowmappings',
        'db_alias': 'workflow-db-alias'
    }


