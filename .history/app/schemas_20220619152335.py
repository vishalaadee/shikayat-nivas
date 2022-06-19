from typing import List
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.sql.sqltypes import Date, DateTime,Integer
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

class StudentModel(BaseModel):    
    block:str
    branch:str
    email: EmailStr
    name : str
    phone:str
    room:str
    
    usn  : str
    srn:str
    sem:int
    class Config:
        orm_mode= True
        
class ComplainModel(BaseModel):    
    topic:str
    description:str
    class Config:
        orm_mode=True

class EmailSchema(BaseModel):
   email: List[EmailStr]
   class config:
        orm_mode=True
        arbitrary_types_allowed = True
        

class RegisterStudent(BaseModel):
    usn:str
    email:EmailStr
        
class MessageSchema(BaseModel):
    subject: str
    body: str
    sender: str
    recipient: List[EmailStr]

class Settings(BaseModel):
    authjwt_secret_key:str='2e5e1aba5ca352882e6a71e553bac6eb71a6b4fae15927e3bee3e0b5394e27b5'


class LoginModel(BaseModel):
    usn:str
    password:str
