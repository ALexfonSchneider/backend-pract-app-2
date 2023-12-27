from sqlalchemy.orm import (
    DeclarativeBase,
    relationship
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    
)

from database import Base


class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', ForeignKey("user.id"))
    description = Column('description', String)
    closed = Column('closed', Boolean, default=False)
