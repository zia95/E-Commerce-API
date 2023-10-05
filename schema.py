from pydantic import BaseModel, EmailStr
from typing import List, Optional



class PostBase(BaseModel):
    title: str
    body: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserCreateResp(BaseModel):
    id: int

class User(BaseModel):
    email: EmailStr

class Post(PostBase):
    id: int

class PostCreate(PostBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
    
class ProductBase(BaseModel):
    prod_name:str
    prod_description:str
    prod_size:int
    prod_total_cost:int
    prod_category:str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

class PriceBase(BaseModel):
    description:str
    price:int
    units:int
    product_id:int

class PriceCreate(PriceBase):
    pass

class OrderBase(BaseModel):
    user_id:int
    delivery_address:str
    notes:str
    total_cost:int

class OrderCreate(OrderBase):
    pass

class Order(ProductBase):
    id: int
    
class SalesBase(BaseModel):
    order_id:int
    product_id:int
    quantity:int

class SalesCreate(SalesBase):
    pass

class Sales(SalesBase):
    id: int

class Revenue(BaseModel):
    total_records_processed: int
    total_cost: float
    total_sale_rate: float
    revenue: float

class Stocks(BaseModel):
    product_id: int
    total: float
    sold: float
    remaining: float
