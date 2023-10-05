from typing import List
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schema import Post, PostCreate, UserCreate, Token, User, UserCreateResp
import utils as utl

from dborm import get_db
from sqlalchemy.orm import Session
import models

router = APIRouter(prefix='/users', tags=['users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserCreateResp)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.password = utl.hash(user.password)
    usr = models.User(**user.model_dump())
    
    db.add(usr)
    db.commit()
    db.refresh(usr)
    
    if not usr:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=usr)
    
    return usr
@router.get('/', response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    usr = db.query(models.User).all()
    return usr

@router.get('/{id}', response_model=User)
def get_user(id:int, db: Session = Depends(get_db)):
    
    usr = db.query(models.User).filter(models.User.id == id).first()
    
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} not found')
    
    
    return usr


@router.post('/login/', status_code=status.HTTP_201_CREATED, response_model=Token)
def login_user(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    usr = db.query(models.User).filter(models.User.email == user.username).first()
    
    if not usr:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user not found')
    
    if not utl.verify(user.password, usr.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user not found')
    
    access_token = utl.create_access_token({utl.USER_ID_K:usr.id})
    return {'access_token': access_token, 'token_type': 'bearer'} 