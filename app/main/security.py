from app.main.model.user import User
from app.main.user_database import user_db_session

def authenticate(username, password):
    '''
    Authenticates a user by email and password
    '''
    session = user_db_session()  
    user = session.query(User).filter(User.uemail == username).first()
    session.close()
    if user and user.check_password(password):
        return user

def identity(payload):
    '''
    Gets the user identity from the decoded payload received from
    the JWT.
    '''
    session = user_db_session()  
    user_id = payload['id']
    user = session.query(User).filter(User.uid == user_id).first()
    session.close()
    return user


