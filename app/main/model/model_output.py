import mongoengine as db

class ModelOutput(db.Document):
    _id = db.StringField(primary_key=True)
    modelID = db.StringField(required=True)
    varName = db.StringField(required=True, unique=True)
    varBenchMarks = db.ListField(required=False)
    varinfo = db.ListField(required=False)
    varValue = db.DynamicField(required=False)
    meta = {
        'collection': 'output-catalog',   
        'db_alias': 'swim-db-alias'
    }