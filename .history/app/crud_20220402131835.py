import json
import ast
from typing import List
from sqlalchemy.orm import Session  # type: ignore
from . import models, schemas

def get_user(db: Session, cid: int):
    return db.query(models.Company).filter(models.Company.cid == cid).first()

def get_item_by_usn(db: Session, USN: str):
    USN=USN.upper()
    return db.query(User).filter_by(usn=USN).first()
