# coding:utf-8
from Base_class.Dynamic_Permission import Dynamic_permission
from Base import Base, db_session
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship


class Specie(Dynamic_permission, Base):
    """分类资源，包含分类名，图片地址，描述（种类描述），父ID（指向某个Speice资源），自ID,tag（级别描述）"""
    db_session = db_session
    __tablename__ = 'Specie'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    tag = Column(String(10))
    name = Column(String(140))
    img_url = Column(String(140))
    describe = Column(String(140))
    suppliers = relationship('Association_specie_supplier', back_populates='specie')
    order = relationship('Association_specie_order', back_populates='specie')
    __in_exclude__ = ['id']

    def __str__(self):
        return self.name