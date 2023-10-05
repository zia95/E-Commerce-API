from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from schema import Post, PostCreate, UserCreate, ProductCreate, PriceCreate, Stocks
import utils as utls
from typing import List
from dborm import get_db
from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.orm import Session
import models

router = APIRouter(prefix='/inventory', tags=['inventory'])

@router.get('/', response_model=List[Stocks])
def get_stocks(db: Session = Depends(get_db)):
    products = db.query(models.Inventory).all()
    sales = db.query(models.Sales).all()
    
    stocks_list = []
    
    for p in products:
        stockdict = {}
        stockdict["product_id"] = p.id
        stockdict["total"] = p.prod_size
        stockdict["sold"] = 0
        for s in sales:
            if s.product_id == p.id:
                price = db.query(models.Price).filter(models.Price.product_id == p.id).order_by(models.Price.created_at.desc()).first()
                stockdict["sold"] = s.quantity * price.units
        
        stockdict["remaining"] = stockdict["total"] - stockdict["sold"]
        stocks_list.append(stockdict)
    
    return stocks_list

#@router.get('/{int}')
#def get_inventory(id: int, db: Session = Depends(get_db)):#.filter(id == models.Inventory.id)
#    products_q = db.query(models.Inventory, models.Price).filter(models.Inventory.id == id).join(models.Price, models.Price.product_id == models.Inventory.id, isouter=True)
#    #q = select(models.Inventory.id, models.Inventory.product_name, models.Inventory.desc, models.Inventory.size, 
#    #           models.Price.price, models.Price.quantity).select_from(
#    #               models.Inventory).join(models.Price, models.Price.product_id == models.Inventory.id)
#    
#    print(products_q)
#    d = products_q.scalar()
#    return d

@router.get('/products')
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Inventory).all()
    return products

@router.post('/products', status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    
    res = models.Inventory(**product.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)
    
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res)
    
    return res

@router.put('/products/{int}')
def update_product(id:int, product:ProductCreate, db: Session = Depends(get_db)):
    product_q = db.query(models.Inventory).filter(models.Inventory.id == id)
    
    if not product_q.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'product with id {id} not found')
    
    product_q.update(product.model_dump(), synchronize_session=False)
    db.commit()
    
    return product_q.first()

@router.get('/prices')
def get_prices(db: Session = Depends(get_db)):
    prices = db.query(models.Price).all()
    return prices

@router.post('/prices', status_code=status.HTTP_201_CREATED)
def add_price(price: PriceCreate, db: Session = Depends(get_db)):
    product = db.query(models.Inventory).filter(models.Inventory.id == price.product_id).first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'product with id {price.product_id} not found')
    
    res = models.Price(**price.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)
    
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res)
    
    return res

