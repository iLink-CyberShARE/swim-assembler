import mongoengine as db

class ModelParameter(db.Document):
    _id = db.StringField(primary_key=True)
    modelID = db.StringField(required=True)
    dataType = db.StringField(required=True)
    paramName = db.StringField(required=True)
    definitionType = db.StringField(required=True)
    structDimension = db.StringField(required=False)
    maxValue = db.IntField(required=True)
    minValue = db.IntField(required=True)

    structType = db.StringField(required=True)
    paraminfo = db.ListField(required=True)
    paramBenchMarks = db.ListField(required=False)
    paramDefaultValue = db.DynamicField(required=False)
    paramValue = db.DynamicField(required=False)
    
    # for visualizations (needs revision)
    widget = db.DynamicField(required=False)
    stepSize = db.DecimalField(required=False)

    # deprecated fields (revise and to remove from db)
    paramLabel =  db.StringField(required=False)
    paramDefaultSource = db.StringField(required=False)
    paramCategory = db.StringField(required=False)

    meta = {
        'collection': 'parameter-catalog',   
        'db_alias': 'swim-db-alias'
    }