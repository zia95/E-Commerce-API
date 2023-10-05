from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from schema import Post, PostCreate, UserCreate
from typing import Optional
#import dbhelper as db
from routers import posts, users, sales, inventory
from dborm import engine, SessionLocal
import models
import utils as utls
from dborm import get_db
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
import json

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

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(sales.router)
app.include_router(inventory.router)

@app.get('/')
async def root():
    return { 'message': 'hello!!' }

@app.get('/loaddummy')
async def load_dummy(db: Session = Depends(get_db)):
    userslist = []
    productslist = []
    
    
    with open('./data/users.json') as f: 
        users_j = json.load(f)
        for u in users_j:
            usr = models.User(email = u["email"], password = utls.hash(u["password"]))
            db.add(usr)
            db.commit()
            db.refresh(usr)
            userslist.append(usr)
    
    with open('./data/products.json') as f: 
        prod_j = json.load(f)
        for p in prod_j:
            prod = models.Inventory(prod_name = p["name"], prod_description = p["description"], prod_size = p["size"], 
                                    prod_total_cost = p["total_cost"], prod_category = p["category"])
            db.add(prod)
            db.commit()
            db.refresh(prod)
            productslist.append(prod)
    
    with open('./data/price.json') as f: 
        price_j = json.load(f)
        for i in range(len(productslist)):
            prc = price_j[i]
            price = models.Price(description = prc["description"], price = prc["price"], units = prc["units"], product_id = productslist[i].id)
            db.add(price)
            db.commit()
    
    with open('./data/orders.json') as f: 
        order_j = json.load(f)
        def __add_order(orderjson, usr, prodidxlst, quantitylist):
            order = models.Order(user_id = usr, delivery_address = orderjson["delivery_address"], notes = orderjson["notes"], total_cost = orderjson["total_cost"])
            db.add(order)
            db.commit()
            db.refresh(order)
            for pi in range(len(prodidxlst)):
                prod = productslist[prodidxlst[pi]]
                quant = quantitylist[pi]
                sales = models.Sales(order_id = order.id, product_id = prod.id, quantity = quant)
                db.add(sales)
                db.commit()
                db.refresh(sales)
        
        __add_order(order_j[10], None,              [2, 4, 8], [1, 2, 1])
        __add_order(order_j[2], userslist[1].id,    [8], [1])
        __add_order(order_j[4], userslist[3].id,    [9, 5], [10, 5])
        __add_order(order_j[23], None,              [0, 3], [2, 5])
        __add_order(order_j[65], userslist[5].id,   [4], [7])
        __add_order(order_j[77], None,              [2, 4, 8, 3], [1, 2, 5, 9])
    
    #with open('./data/orders.json') as f: orders_j = json.load(f)
    #
    #for l in orders_j:
    #    print(l)
    #
    #usr1 = models.User(email="user1@test.com", password=utls.hash("password"))
    #usr2 = models.User(email="user2@test.com", password=utls.hash("password"))
    #usr3 = models.User(email="user3@test.com", password=utls.hash("password"))
    #usr4 = models.User(email="user4@test.com", password=utls.hash("password"))
    #usr5 = models.User(email="user5@test.com", password=utls.hash("password"))
    #
    #db.add_all([
    #        usr1, 
    #        usr2, 
    #        usr3, 
    #        usr4, 
    #        usr5
    #        ])
    #db.commit()
    #
    #
    #prod1 = models.Inventory(product_name="product 1", desc="product 1", size=9)
    #prod2 = models.Inventory(product_name="product 2", desc="product 2", size=99)
    #prod3 = models.Inventory(product_name="product 3", desc="product 3", size=55)
    #prod4 = models.Inventory(product_name="product 4", desc="product 4", size=65)
    #prod5 = models.Inventory(product_name="product 5", desc="product 5", size=2)
    #
    #db.add_all([
    #        prod1, 
    #        prod2, 
    #        prod3, 
    #        prod4, 
    #        prod5
    #        ])
    #db.commit()
    #db.refresh(prod1)
    #db.refresh(prod2)
    #db.refresh(prod3)
    #db.refresh(prod4)
    #db.refresh(prod5)
    #
    #price1 = models.Price(desc="price 1", price=  10, quantity=1, product_id=prod1.id)
    #price2 = models.Price(desc="price 2", price=  50, quantity=1, product_id=prod2.id)
    #price3 = models.Price(desc="price 3", price= 260, quantity=1, product_id=prod3.id)
    #price4 = models.Price(desc="price 4", price= 340, quantity=1, product_id=prod4.id)
    #price5 = models.Price(desc="price 5", price=1000, quantity=1, product_id=prod5.id)
    #
    #db.add_all([
    #        price1, 
    #        price2, 
    #        price3, 
    #        price4, 
    #        price5
    #        ])
    
    return { 'status': 'successfully loaded dummy data in database.' }

@app.get('/resetdb')
async def reset_db(db: Session = Depends(get_db)):
    db.query(models.Post).delete(synchronize_session=False)
    db.query(models.User).delete(synchronize_session=False)
    db.query(models.Log).delete(synchronize_session=False)
    db.query(models.Price).delete(synchronize_session=False)
    db.query(models.Inventory).delete(synchronize_session=False)
    db.query(models.Sales).delete(synchronize_session=False)
    db.query(models.Order).delete(synchronize_session=False)
    db.commit()
    
    return { 'status': 'successfully cleared db' }



