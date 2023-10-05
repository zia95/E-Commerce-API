from dborm import Base, SessionLocal, SQLALCHEMY_CONNECTION_STRING
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(String(4096), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Log(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, nullable=False)
    log = Column(String(255), nullable=False)

class Price(Base):
    __tablename__ = "prices"
    
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String(2048), nullable=False)
    price = Column(Integer, nullable=False)
    units = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("inventory.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, nullable=False)
    prod_name = Column(String(256), nullable=False)
    prod_description = Column(String(2048), nullable=False)
    prod_size = Column(Integer, nullable=False)
    prod_total_cost = Column(Integer, nullable=False)
    prod_category = Column(String(256), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Sales(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("inventory.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    delivery_address = Column(String(255), nullable=False)
    notes = Column(String(256), nullable=True)
    total_cost = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
