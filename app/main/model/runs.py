import mongoengine as db

class Run(db.Document): 
    _id = db.StringField(primary_key=True)
    runid = db.StringField(required=True, unique=True)
    flowid = db.StringField(required=True)
    modelid = db.StringField(required=True)

    meta = {
        'collection': 'runs',
        'db_alias': 'workflow-db-alias'
    }
