import hashlib
from werkzeug.security import safe_str_cmp
from app.main.user_database import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    """ Users table """
    __tablename__ = "USER"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    uemail = Column(String)
    upassword = Column(String)
    is_guest = Column(Boolean)
    is_contentmanager = Column(Boolean)

    def check_password(self, password):
        encoded_password = password.encode()
        hashed_password = hashlib.sha1(encoded_password).hexdigest()
        return safe_str_cmp(self.upassword, hashed_password)

    def __repr__(self):
        return "<User '{}'>".format(self.uid)
