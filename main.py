from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from schema import Post, PostCreate, UserCreate
from typing import Optional
#import dbhelper as db
from routers import posts, users, sales, inventory
from dborm import engine, SessionLocal
import models

from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

allowed_ori=[]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_ori,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return { 'message': 'hello!!' }


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(sales.router)
app.include_router(inventory.router)
