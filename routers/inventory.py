from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from schema import Post, PostCreate, UserCreate
import utils as utls
from typing import List
from dborm import get_db
from sqlalchemy.orm import Session
import models

router = APIRouter(prefix='/inventory', tags=['inventory'])

@router.get('/')
def get_inventory(db: Session = Depends(get_db)):
    return {"inv.test":"test"}
