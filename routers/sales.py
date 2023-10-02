from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from schema import Post, PostCreate, UserCreate
import utils as utls
from typing import List
from dborm import get_db
from sqlalchemy.orm import Session
import models

router = APIRouter(prefix='/sales', tags=['sales'])

@router.get('/')
def get_sales(db: Session = Depends(get_db)):
    return {"sales.test":"test"}
