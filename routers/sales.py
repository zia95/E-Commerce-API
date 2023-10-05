from datetime import datetime
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from schema import Post, PostCreate, UserCreate, OrderCreate, SalesCreate, Revenue
import utils as utls
from typing import List, Optional
from dborm import get_db
from sqlalchemy.orm import Session
import models

router = APIRouter(prefix='/sales', tags=['sales'])


@router.get('/orders/')
def get_orders(limit:int = 5, offset:int = 0, start_date: Optional[datetime] = "2020-09-22T18:07:13", end_date: Optional[datetime] = "2024-09-22T18:07:13", db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.created_at.between(start_date, end_date)).limit(limit).offset(offset).all()
    return orders

@router.get('/orders/{id}')
def get_orderdetails(order_id: int, db: Session = Depends(get_db)):
    orders = db.query(models.Sales).filter(models.Sales.order_id == order_id).all()
    return orders

@router.get('/orders/')
def get_orderdetails(category: Optional[str] = None, limit:int = 5, offset:int = 0, 
                 start_date: Optional[datetime] = "2020-09-22T18:07:13", end_date: Optional[datetime] = "2024-09-22T18:07:13", 
                 db: Session = Depends(get_db)):
    
    sales_q = db.query(models.Sales).filter(models.Sales.created_at.between(start_date, end_date))
    
    if(category != None):
        prod = db.query(models.Inventory).filter(models.Inventory.prod_category.ilike(category)).all()
        pids = [p.id for p in prod]
        sales_q = sales_q.filter(models.Sales.product_id.in_(pids))
    
    return sales_q.limit(limit).offset(offset).all()

@router.get('/revenue', response_model=Revenue)
def calc_revenue(category: Optional[str] = None,
                 start_date: Optional[datetime] = "2020-09-22T18:07:13", 
                 end_date: Optional[datetime] = "2024-09-22T18:07:13", 
                 db: Session = Depends(get_db)):
    sales = db.query(models.Sales).filter(models.Sales.created_at.between(start_date, end_date)).all()
    
    prod_q = db.query(models.Inventory).filter(models.Inventory.id.in_([o.product_id for o in sales])) 
    if(category != None):
        prod_q = prod_q.filter(models.Inventory.prod_category.ilike(category))
    
    prod = prod_q.all()
    
    total_records_processed = 0
    total_cost = 0
    total_sale_rate = 0
    
    for s in sales:
        for product in prod:
            if s.product_id == product.id:
                price = db.query(models.Price).filter(models.Price.product_id == product.id).order_by(models.Price.created_at.desc()).first()
                cost_per_unit = (product.prod_total_cost / product.prod_size)
                total_cost += cost_per_unit * (price.units * s.quantity)
                total_sale_rate += price.price * s.quantity
                total_records_processed += 1
    
    return { "total_records_processed": total_records_processed, "total_cost": total_cost, "total_sale_rate": total_sale_rate, "revenue": total_sale_rate - total_cost}

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, products: List[SalesCreate], db: Session = Depends(get_db)):
    return {"status": "not_implemented"}
    res = models.Order(**order.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)
    
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res)
    
    return res
