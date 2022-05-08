from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.sqltypes import Date, DateTime, Float,Integer
from .database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey

    
class User(Base):
    __tablename__='students'
    usn=Column(String(12),primary_key=True,unique=True)
    name=Column(String(100),unique=False)
    srn=Column(Integer,unique=True)
    block=Column(String(5),unique=False)
    room=Column(Integer,unique=False)
    email=Column(String(80),unique=False)
    branch=Column(String(25),unique=False)
    sem=Column(Integer,unique=False)
    phone=Column(String(14),unique=False)
    secondary_phone=Column(String(14),unique=False)
    def __repr__(self):
        return f"<User {self.name}"


class Credentials(Base):
    __tablename__ = 'credentials'
    usn=Column(String(12),primary_key=True,unique=True)
    password=Column(String(50),unique=False)
    valid=Column(Boolean,default=True)

class complains(Base):
    __tablename__ = 'complains'
    cid=Column(Integer,primary_key=True,unique=True)
    usn=Column(String(12),ForeignKey('students.usn'))
    topic=Column(String(100),unique=False)
    description=Column(String(500),unique=False)
    feedback=Column(String(500),unique=False)
    status=Column(Integer,unique=False)
    date