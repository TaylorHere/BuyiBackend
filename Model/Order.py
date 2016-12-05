from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from Base_class.Dynamic_Permission import Dynamic_permission
from Base import db_session, Base


class Order(Base, Dynamic_permission):
    db_session = db_session
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
