import mongoengine as db

class ModelSet(db.Document):
    _id = db.StringField(primary_key=True)
    modelID = db.StringField(required=True)
    setName = db.StringField(required=True)
    setValue = db.StringField(required=True)
    setLabel = db.StringField(required=True)
    setDescription = db.StringField(required=True)
    meta = {
        'collection': 'set-catalog',   
        'db_alias': 'swim-db-alias'
    }