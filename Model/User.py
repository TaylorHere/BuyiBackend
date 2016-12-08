# coding:utf-8
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from passlib.hash import pbkdf2_sha256 as pwd_context
import time
import random
from Base import Base, db_session
from SinglePage.singlepage import *
import uuid

class User(GeneralViewWithSQLAlchemy, Base):
    """用户资源，创建时需要pwd会被hashed，这会花费一定时间"""
    db_session = db_session
    __tablename__ = 'User'

    class SEX_CHOICE():
        FEMALE = 'female'
        MALE = 'male'
        UNKNOWN = 'unknown'

    id = Column(Integer, primary_key=True)
    telephone = Column(String(15), unique=True, nullable=False)
    nickname = Column(String(20))
    sex = Column('sex', Enum(SEX_CHOICE.FEMALE,
                             SEX_CHOICE.MALE, SEX_CHOICE.UNKNOWN))
    img_url = Column(String(1000))
    openid = Column(String(125), unique=True, nullable=False)
    password = Column(String(256))
    permissions = relationship('Permission', backref='User')

    def __str__(self):
        return self.nickname

    def pwd_verify(self, password):
        return pwd_context.verify(password, self.password)

    def __init__(self):
        self.openid = str(uuid.uuid1())
        super(User, self).__init__()

    @property
    def pwd(self):
        return self.password

    @pwd.setter
    def pwd(self, value):
        self.password = pwd_context.hash(value)

    __property__ = {'pwd': 'password'}
    __in_exclude__ = ['id', 'role', 'password', 'openid']
    # 定义哪些字段不展示给前端
    __exclude__ = ['password']
