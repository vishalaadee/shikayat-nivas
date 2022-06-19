from typing import List
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.sql.sqltypes import Date, DateTime,Integer
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

class StudentModel(BaseModel):    
    usn  : str
    name : str
    email: EmailStr
    srn:int
    block:str
    room:int
    branch:str
    sem:int
    phone:str
    secondary_phone:str
    class Config:
        orm_mode= True
                Schema_extra={
            'example':{
            'cname':'Fidelity',
            'category':'TIER-1',
            'package':'1000000.00',
            'internship_stipend':'10000',
            'deadline':'2020-02-01',
            'date':'2020-01-01',
            'ssc':'60.00',
            'hsc':'60.00',
            'ug':'7.00',
            'pg':'7.00',
            'branch':'CSE',
            'backlogs':'0',
            'gender':'M,F'
                    }
        }
    
        
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
