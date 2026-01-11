
from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from ..schemas.user_schema import user_schema
from dependencies import getdb
from ..models.user import users
from passlib.context import CryptContext
router= APIRouter(
         prefix="/Auth",
         tags= ["Auth"]
)

context= CryptContext(schemes=['argon2'], deprecated="auto")

def hash_password(passwod: str):
      return context.hash(passwod)

@router.post('/signup')
def register(inserted_user: user_schema,db:Session= Depends(getdb)):
    user_in_db= db.query(users).filter(users.username== inserted_user.username).first()
    if user_in_db:
        raise HTTPException(status_code=409, detail="User already Exist try login")
    hashed_password= hash_password(inserted_user.password)
    user_db=users(
         username= inserted_user.username,
         passwordhash= hashed_password
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return inserted_user