#coding:utf-8
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from Base_class.Dynamic_Permission import Dynamic_permission
from Base import db_session, Base


class Order(Base, Dynamic_permission):
    """订单类，提供商品和溯源信息	"""
    db_session = db_session
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
    price = Column(String)
    supplier_market = relationship('Association_supplier_market',back_populates='order')
    market_pedlar = relationship('Association_market_pedlar',back_populates='order')

    __in_exclude__ = ['id']