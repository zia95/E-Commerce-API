from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from schema import Post, PostCreate, UserCreate
import utils as utls
from typing import List
from dborm import get_db
from sqlalchemy.orm import Session
import models

router = APIRouter(prefix='/posts', tags=['posts'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db), curr_usr: int = Depends(utls.get_current_user)):
    
    res = models.Post(**post.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)
    
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res)
    
    return res

@router.get('/', response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get('/{id}')
def get_post(id:int, db: Session = Depends(get_db)):
    pst = db.query(models.Post).filter(models.Post.id == id).first()
    if not pst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')
    return pst

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    res = db.query(models.Post).filter(models.Post.id == id)
    
    if not res.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')
    
    res.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{int}')
def update_post(id:int, post:PostCreate, db: Session = Depends(get_db)):
    pst_q = db.query(models.Post).filter(models.Post.id == id)
    
    if not pst_q.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')
    
    pst_q.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return pst_q.first()