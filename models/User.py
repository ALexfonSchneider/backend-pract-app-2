from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from database import Base


class User(Base):
    __tablename__ = 'users'
    
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    email = Column('email', String)
    join_date = Column('join_date', DateTime, default=datetime.now)
    password_hash = Column('password_hash', String)