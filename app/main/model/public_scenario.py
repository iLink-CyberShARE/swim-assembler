import mongoengine as db
from .model_output import ModelOutput
from .model_parameter import ModelParameter
from .model_set import ModelSet

class PublicScenario(db.Document):
    _id = db.StringField(primary_key=True)
    _cls = db.StringField(required=False)
    className = db.StringField(required=False)
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    isPublic = db.BooleanField()
    userid = db.StringField(required=False)
    start = db.StringField(required=False)
    startedAtTime = db.StringField(null=True)
    endedAtTime = db.StringField(null=True)
    status =  db.StringField(required=True)
    modelSettings = db.ListField(required=True)
    modelSets = db.ListField(required=False)
    modelInputs = db.ListField(required=True)
    modelOutputs = db.ListField(required=False)
    meta = {
        'collection': 'public-scenarios',
        'db_alias': 'swim-db-alias'
    }