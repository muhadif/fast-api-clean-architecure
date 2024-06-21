from pydantic import BaseModel
from datetime import datetime


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime


class SignInRequest(BaseModel):
    access_token: str
    expiration: str
