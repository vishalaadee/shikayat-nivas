from . import crud,models, schemas
from typing import List
from sqlalchemy import insert
from fastapi.exceptions import HTTPException
from fastapi import APIRouter,status,Depends
from .models import User,Credentials,complains
from .database import Session, engine
from .schemas import StudentModel,LoginModel,RegisterStudent,EmailSchema,MessageSchema,Settings,ComplainModel

admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
    )

session=Session(bind=engine)


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

@admin_router.post("/home/status/{cid}",status_code=status.HTTP_201_CREATED)
async def status_user(cid:int,status:int,db:Session=Depends(get_db)):
    dc=db.query(complains).filter(complains.cid==cid).all()
    if dc is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint doesn't exists"
        )
    
    dc[0].status=status
    db.commit()
    return {"message":"Status updated"}    

@admin_router.post("/home/block/{cid}",status_code=status.HTTP_201_CREATED)
async def block_user(cid:int,db:Session=Depends(get_db)):
    dc=db.query(complains.usn).filter(complains.cid==cid).all()
    if dc is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint doesn't exists"
        )
    dp=db.query(Cre).filter(User.usn==dc[0].usn).first()
    dc[0].valid=False
    db.commit()
    return {"message":"Status updated"}
