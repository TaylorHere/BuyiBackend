#coding:utf-8
from Base_class.Dynamic_Permission import Dynamic_permission
from Base import Base,db_session
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
class Association_specie_supplier(Dynamic_permission,Base):
	"""供应商供应的种类信息，使用此接口查询和添加供应商经营的种类"""
	db_session = db_session
	__tablename__ = 'Association_specie_supplier'

	specie_id = Column(Integer,ForeignKey('Specie.id'),primary_key=True)
	supplier_id = Column(Integer,ForeignKey('Supplier.id'),primary_key=True)

	specie = relationship('Specie', back_populates='suppliers')
	supplier = relationship('Supplier', back_populates='species')