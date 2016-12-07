#coding:utf-8
from Base_class.Dynamic_Permission import Dynamic_permission
from Base import Base,db_session
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
class Market(Dynamic_permission,Base):
	"""市场接口，包含址信息，tag信息"""
	db_session = db_session
	__tablename__ = 'Market'

	id = Column(Integer, primary_key=True)
	name = Column(String(200))
	suppliers = relationship('Association_supplier_market', back_populates='market')
	pedlar = relationship('Association_market_pedlar', back_populates='market')
	__in_exclude__ = ['id']