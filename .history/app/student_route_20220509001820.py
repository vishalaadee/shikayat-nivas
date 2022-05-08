from distutils.ccompiler import new_compiler
from fastapi import UploadFile, File,APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.exceptions import HTTPException
from fastapi import APIRouter,status,Depends
import pytz
import boto3
import ast
from datetime import datetime, timezone
import json
from typing import List
import databases
from sqlalchemy.orm import Session 
from .models import User,Credentials,complains
from .database import Session, engine
from .schemas import StudentModel,LoginModel,RegisterStudent,EmailSchema,MessageSchema,Settings,ComplainModel
from . import models, schemas,crud


models.Base.metadata.create_all(bind=engine)
itemrouter = APIRouter(    
    prefix='/student',
    tags=['student']
)



def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
        
@itemrouter.post("/home/edit_user/{usn}",status_code=status.HTTP_201_CREATED)
async def update_user(user:StudentModel,usn:str,db:Session=Depends(get_db)):
    usn=usn.upper()
    usn=usn.strip()
    dc=db.query(User).filter(User.usn==usn).first()
    if dc is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exists"
        )
    dc.usn=user.usn.upper(),
    dc.email=user.email,
    dc.name=user.name,
    dc.srn=user.srn,
    dc.block=user.block,
    dc.room=user.room,
    dc.branch=user.branch,
    dc.sem=user.sem,
    dc.phone=user.phone,
    dc.secondary_phone=user.secondary_phone
    
       
    db.commit()
    
    return {"message":"Student Details Updated"}

@itemrouter.post("/home/register_complain/{usn}",status_code=status.HTTP_201_CREATED)
async def complain_user(user:ComplainModel,usn:str,db:Session=Depends(get_db)):

    new_complain=complains(
        usn=usn
        topic=user.topic,
        description=user.description,
        status=0
    ) 
    db.add(new_complain)

    db.commit()
    
    return {"message":"Complaint Registered"}

@itemrouter.get("/home/status_complain/{usn}/{cid}",status_code=status.HTTP_201_CREATED)
async def status_user(usn:str,cid:int,db:Session=Depends(get_db)):
    dc=db.query(complains).filter(complains.cid==cid).all()
    if dc is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint doesn't exists"
        )
    return dc

@itemrouter.get("/home/re_complain/{usn}/{cid}",status_code=status.HTTP_201_CREATED)
async def re_complain_user(usn:str,cid:int,db:Session=Depends(get_db)):
    dc=db.query(complains).filter(complains.cid==cid).all()
    if dc is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint doesn't exists"
        )
    dc.update({"status":1})
    db.commit()
    return {"message":"Complaint Re-Opened"}    

@itemrouter.post("/home/feedback_complain/{usn}/{cid}",status_code=status.HTTP_201_CREATED)
async def feedback_user(user:ComplainModel,usn:str,cid:int,db:Session=Depends(get_db)):
    dc=db.query(complains).filter(complains.cid==cid).all()
    if dc is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint doesn't exists"
        )
    if dc.status==2:  
        new_complain=complains(
        feedback=user.feedback
    ) 
        dc.commit()
    
        return {"message":"Feedback Registered"}

    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
   



