# coding:utf-8
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from Base_class.Dynamic_Permission import Dynamic_permission
from Base import db_session, Base
from Model.Specie import Specie
import time
class Order(Base, Dynamic_permission):
    """订单类，提供商品和溯源信息	"""
    db_session = db_session
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
    price = Column(String)
    quantity = Column(String)
    rank = Column(String)
    _creat_time = Column(String)

    specie = relationship(
        'Association_specie_order', back_populates='order')
    supplier_market = relationship(
        'Association_supplier_market', back_populates='order')
    market_pedlar = relationship(
        'Association_market_pedlar', back_populates='order')
    @property
    def creat_time(self):
        return self._creat_time
    @creat_time.setter
    def creat_time(self,value):
        self._creat_time = str(int(time.time()*1000))
    @property
    def name(self):
        name = []
        for s in self.specie:
            name.append(s.specie.name)
        return name
    @property
    def species(self):
        specie = []
        for s in self.specie:
            specie = db_session.query(Specie).filter(Specie.id == s.specie.parent_id).all()
        return specie
    @property
    def supplier(self):
        sup = []
        for sm in self.supplier_market:
            sup.append(sm.supplier.name)
        return sup
    @property
    def markets(self):
        mar = []
        for mp in self.market_pedlar:
            mar.append(mp.market.name)
        return mar
    @property
    def pedlars(self):
        ped = []
        for mp in self.market_pedlar:
            ped.append(mp.pedlar.name)
        return ped
    __in_exclude__ = ['id','_creat_time','pedlars','markets','supplier','name','species']
    __exclude__ = ['_creat_time']
    __property__ = {
        'creat_time':'_creat_time',
        'pedlars':'',
        'markets':'',
        'supplier':'',
        'name':'',
        'species':''
        }