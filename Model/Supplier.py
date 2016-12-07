# coding:utf-8
from Base_class.Dynamic_Permission import Dynamic_permission
from Base import Base, db_session
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship


class Supplier(Dynamic_permission, Base):
    """供应商接口，包含址信息，tag信息"""
    db_session = db_session
    __tablename__ = 'Supplier'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    address = Column(String(200))
    tag = Column(String(200))
    species = relationship('Association_specie_supplier', back_populates='supplier')
    markets = relationship('Association_supplier_market', back_populates='supplier')
    __in_exclude__ = ['id']
