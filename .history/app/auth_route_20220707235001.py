import email,io,ast,json
from io import BytesIO
from fastapi import File,UploadFile,Form,Body,Response,FastAPI, BackgroundTasks,APIRouter,status,Depends
from fastapi.responses import StreamingResponse
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List, Optional
from fastapi.exceptions import HTTPException
from .models import User,Credentials,complains
from .database import Session, engine
from .schemas import StudentModel,LoginModel,RegisterStudent,EmailSchema,MessageSchema,Settings,ComplainModel
from werkzeug.security import generate_password_hash , check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from . import  crud,models, schemas
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
    )

session=Session(bind=engine)


def generate_password():
    import random
    import array

    MAX_LEN = 6

    
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    SYMBOLS = ['@','(', ')', '<']

    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
    temp_pass_list = array.array('u', temp_pass)
    random.shuffle(temp_pass_list)

    password = ""
    for x in temp_pass_list:
        password = password + x
    return password


conf = ConnectionConfig(
    MAIL_USERNAME = "placementsjce2022@gmail.com",
    MAIL_PASSWORD = "hdrpsazaxupdkjxm",
    MAIL_FROM = "placementsjce2022@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Placement-Information",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
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
        

session=Session(bind=engine)

@auth_router.post('/auth/admin_login',status_code=200)
async def admin_login(usn:str,password:str,Authorize:AuthJWT=Depends()):
    usn=usn.upper()
    usn=usn.strip()
    password=password.upper()
    password=password.strip()
    if usn=="SJCEHOSTEL00" and password=="JSSSTU":
        access_token=Authorize.create_access_token(subject=password)
        refresh_token=Authorize.create_refresh_token(subject=password)

        response={
            "access":access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Password"
    )
    return 
@auth_router.post("/auth/register",status_code=status.HTTP_201_CREATED)
async def register(usn:str,email: EmailStr,db: session = Depends(get_db)) -> JSONResponse:
     usn=usn.upper()
     usn=usn.strip()
     email=email.strip()
     if usn!=None and email!=None:
        a=generate_password()
        message = MessageSchema(
            subject="Password Set Link",
            recipients=[email],  # List of recipients, as many as you can pass 
            body="your password is "+a,
        
            )
        a=generate_password_hash(a)
        credentials=Credentials(usn=usn,password=a)
        
        new_user=User(
            usn=usn,
            email=email
        ) 

        session.add(new_user)
        session.add(credentials)
        session.commit()
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
     else:
        return JSONResponse(status_code=200, content={"message": "invalid credentials"})

@auth_router.post("/auth/forgot_password",status_code=status.HTTP_201_CREATED)
async def forgot_pass(usn:str,email: EmailStr,db: session = Depends(get_db)) -> JSONResponse:
     usn=usn.upper()
     usn=usn.strip()
     db_email=session.query(User).filter(User.email==email).first()
     db_usn=session.query(User).filter(User.usn==usn).first()
     db_cred=session.query(Credentials).filter(Credentials.usn==usn).first()
     if db_usn and (db_usn.email==email) and db_cred!=None:
        db_user= crud.get_item_by_credentials(db,usn)
        a=generate_password()
        message = MessageSchema(
            subject="Password Set Link",
            recipients=[email],  # List of recipients, as many as you can pass 
            body="your password is "+a,
        
            )
        a=generate_password_hash(a)
        db_user[0].password=a
        db.commit()
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
     elif db_usn and (db_usn.email==email) and (db_cred==None):
        return JSONResponse(status_code=200, content={"message": "Account yet not activated"})
     else:
         return JSONResponse(status_code=200, content={"message": "invalid response"})     

@auth_router.post("/home/password/changepassword/{usn}")
def change_password_student(usn:str,oldpass:str,newpass:str,db:Session=Depends(get_db)):
    usn=usn.upper()
    usn=usn.strip()
    db_user= crud.get_item_by_credentials(db,usn)
    if db_user and check_password_hash(db_user[0].password,oldpass):
        newpass=generate_password_hash(newpass)
        db_user[0].password=newpass
        db.commit()
        return {"message":"Password changed successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong Password")
     
@auth_router.post('/login',status_code=200)
async def login(usn:str,password:str,Authorize:AuthJWT=Depends()):
    usn=usn.upper()
    usn=usn.strip()
    db_user=session.query(Credentials).filter(usn==Credentials.usn).first()
    password=password.strip()
    if db_user.valid==False:
      return JSONResponse(status_code=500, content={"message": "Account Blocked By Warden"})     
    elif db_user and check_password_hash(db_user.password,password):
        access_token=Authorize.create_access_token(subject=db_user.usn)
        refresh_token=Authorize.create_refresh_token(subject=db_user.usn)

        response={
            "access":access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username Or Password"
    )




@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    
    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a valid refresh token"
        ) 

    current_user=Authorize.get_jwt_subject()

    
    access_token=Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access":access_token})
