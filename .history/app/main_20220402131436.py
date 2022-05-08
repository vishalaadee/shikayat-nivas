from fastapi import FastAPI
from .admin_route import admin_router
from .student_route import itemrouter
from .student_route import itemrouter

from fastapi_jwt_auth import AuthJWT
from .schemas import Settings

origins = ["*"]



from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin_router)
app.include_router(itemrouter)
