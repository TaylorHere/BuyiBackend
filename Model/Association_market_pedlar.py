from Base_class.Dynamic_Permission import Dynamic_permission
from Base import Base,db_session
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

import datetime
import uuid
class Association_market_pedlar(Dynamic_permission,Base):
	"""订单于市场方和商贩方关联资源，订单从市场方发货给商贩方，使用此接口"""
	db_session = db_session
	__tablename__ = 'Association_market_pedlar'

	_uuid = Column(String(40),nullable=False, unique=True)
	from_uuid = Column(String(40))

	_creat_time = Column(DateTime)

	market_id = Column(Integer,ForeignKey('Market.id'), primary_key=True)
	pedlar_id = Column(Integer,ForeignKey('Pedlar.id'), primary_key=True)
	order_id = Column(Integer,ForeignKey('Order.id'), primary_key=True)
	market = relationship('Market', back_populates='pedlar')
	pedlar = relationship('Pedlar', back_populates='market')
	order = relationship('Order', back_populates='market_pedlar')

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