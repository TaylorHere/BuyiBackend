# coding:utf-8
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from passlib.apps import custom_app_context as pwd_context

from Base import Base, db_session
from SinglePage.singlepage import *


class Permission(GeneralViewWithSQLAlchemy, Base):
	"""权限与用户关联接口，使用此接口给用户授权"""
    __tablename__ = 'Permission'
    db_session = db_session
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship("User",back_populates='permissions')
    name = Column(String(20))

    def __str__(self):
        return self.name

    __in_exclude__ = ['id']