# coding:utf-8
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from Base_class.Dynamic_Permission import Dynamic_permission
from Base import db_session, Base
from Model.Specie import Specie
import time
from SinglePage.singlepage import GeneralViewWithSQLAlchemy


class Order(Base, GeneralViewWithSQLAlchemy):
    """订单类，提供商品相关信息"""
    db_session = db_session
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
    price = Column(String(10))
    quantity = Column(String(40))
    rank = Column(String(3))
    _creat_time = Column(String(15))

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
    def creat_time(self, value):
        self._creat_time = str(int(time.time()))

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

    __in_exclude__ = ['id', '_creat_time', 'pedlars', 'markets', 'supplier', 'name', 'species']
    __exclude__ = ['_creat_time']
    __property__ = {
        'creat_time': '_creat_time',
        'pedlars': '',
        'markets': '',
        'supplier': '',
        'name': '',
        'species': ''
    }

    def __str__(self):
        return str(self.id)
