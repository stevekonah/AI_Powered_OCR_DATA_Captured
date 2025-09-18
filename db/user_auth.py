import bcrypt
from sqlalchemy import Column, Integer, String
from .database import Base, Session

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)  # user, supervisor, admin

def add_user(username, password, role="user"):
    session = Session()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(username=username, password_hash=password_hash, role=role)
    session.add(user)
    session.commit()
    session.close()

def authenticate_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return user
    return None