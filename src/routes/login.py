


from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from src.services.auth_service import create_token  
from src.schemas.user_schema import user_schema
from src.models.user import users
from dependencies import getdb
from passlib.context import CryptContext
import jwt
import os
from dotenv import load_dotenv
load_dotenv()
router=APIRouter(
    prefix="/Auth",
    tags=["Auth"]
)




context= CryptContext(schemes=["argon2"], deprecated="auto")

def decrypt_password(inserted_pasword: str, hashed_password: str):
    return context.verify(inserted_pasword, hashed_password)

@router.post('/login')
def login(user: user_schema, response: Response, db:Session= Depends(getdb)):
    user_db=db.query(users).filter(users.username == user.username).first()
    if not user_db:
       raise HTTPException(status_code=404, detail="User does not exist")
    if not decrypt_password(user.password , user_db.passwordhash):
        raise HTTPException(status_code=401, detail="Wrong password")
    token = create_token(user_db.username)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,     
        samesite="None",
        path="/"   
    )
    return {"message": "Login successful"}