import os

class Config:
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    USER_DATABASE_URL = os.getenv('USER_DATABASE_URL', "this-is-the-default-URL") 
    MODEL_DATABASE_URL = os.getenv("MODEL_DATABASE_URL", "this-is-the-default-URL") 
    WORKFLOW_DATABASE_URL = os.getenv("WORKFLOW_DATABASE_URL", "this-is-the-default-URL") 
    POOL_PRE_PING = True
    POOL_SIZE = 5
    POOL_RECYCLE= 3600   
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    USER_DATABASE_URL = os.getenv('USER_DATABASE_URL', "this-is-the-default-URL") 
    MODEL_DATABASE_URL = os.getenv("MODEL_DATABASE_URL", "this-is-the-default-URL") 
    WORKFLOW_DATABASE_URL = os.getenv("WORKFLOW_DATABASE_URL", "this-is-the-default-URL") 
    POOL_PRE_PING = True
    POOL_SIZE = 5
    POOL_RECYCLE= 3600   
    DEBUG = True
    TESTING = True

class DevelopmentConfig(Config):
    SECRET_KEY = os.getenv("SECRET_KEY", "yoursecretapikeyhere")
    USER_DATABASE_URL = os.getenv('USER_DATABASE_URL', "mysql://user:password@localhost:3306/userdb") 
    MODEL_DATABASE_URL = os.getenv("MODEL_DATABASE_URL", "mongodb://user:password@localhost:27017/modeldb?authSource=admin") 
    WORKFLOW_DATABASE_URL = os.getenv("WORKFLOW_DATABASE_URL", "mongodb://user:password@localhost:27017/workflowdb?authSource=admin") 
    POOL_PRE_PING = True
    POOL_SIZE = 5
    POOL_RECYCLE= 3600   
    DEBUG = True
    TESTING = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
