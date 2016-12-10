from Base_class.Dynamic_Permission import Dynamic_permission
from Base import Base,db_session
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import uuid
import datetime
class Association_supplier_market(Dynamic_permission,Base):
	"""订单 供应商和市场方关联接口，供应商向市场方发货使用此接口"""
	db_session = db_session
	__tablename__ = 'Association_supplier_market'

	_uuid = Column(String(40),nullable=False, unique=True)
	_creat_time = Column(DateTime)

	market_id = Column(Integer,ForeignKey('Market.id'), primary_key=True ,autoincrement=False)
	supplier_id = Column(Integer,ForeignKey('Supplier.id'), primary_key=True,autoincrement=False)
	order_id = Column(Integer,ForeignKey('Order.id'), primary_key=True)
	order = relationship('Order', back_populates='supplier_market')
	market = relationship('Market', back_populates='suppliers')
	supplier = relationship('Supplier', back_populates='markets')

	@property
	def creat_time(self):
		return self._creat_time
	@creat_time.setter
	def creat_time(self,value):
		self._creat_time = datetime.datetime.now()

	@property
	def uuid(self):
		return self._uuid
	@uuid.setter
	def uuid(self,value):
		self._uuid = str(uuid.uuid1())

	__in_exclude__= ['_uuid','_creat_time']
	__exclude__ = ['_creat_time','_uuid']
	__property__ = {'creat_time':'_creat_time','uuid':'_uuid'}