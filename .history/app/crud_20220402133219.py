import json
import ast
from typing import List
from sqlalchemy.orm import Session  # type: ignore
from .models import User,Credentials,complains
from .database import Session, engine
from .schemas import StudentModel,LoginModel,RegisterStudent,EmailSchema,MessageSchema,Settings,ComplainModel
from . import models, schemas


def get_item_by_usn(db: Session, USN: str):
    USN=USN.upper()
    return db.query(User).filter_by(usn=USN).first()

def get_item_by_credentials(db: Session, usn:str):
    usn=usn.upper()
    return db.query(Credentials).filter_by(usn=usn)
