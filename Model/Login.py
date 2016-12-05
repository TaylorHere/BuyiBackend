# coding: utf-8
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Enum
from sqlalchemy.orm import relationship
import datetime
from User import User
from Base import Base, db_session
from passlib.apps import custom_app_context as pwd_context
from permissions.permissions import can_not_delete_this_rescources, need_json_exclude_get
from SinglePage.singlepage import *


class Login(GeneralViewWithSQLAlchemy, Base):
    """登陆接口，在user接口获取用户openid，传入openid和pwd后获得的base作为其它接口的验证凭据，请将获得的user_id和base放在header中，格式XXX-user-id:1,XXX-base:sdfasdfasd """
    db_session = db_session
    __tablename__ = 'Login'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    _openid = Column(String(125))
    base = Column(String(125))
    login_time = Column(DateTime())
    _pwd = ''

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, value):
        self._pwd = value

    @property
    def openid(self):
        return self._openid

    @openid.setter
    def openid(self, value):
        self._openid = value
        user = self.db_session.query(User).filter(
            User.openid == value).first()
        if user is not None:
            self.pwd = request.get_json()['pwd']
            if user.pwd_verify(self.pwd):
                self.user_id = user.id
                self.base = pwd_context.encrypt(user.pwd)
                self.login_time = datetime.now()

    __property__ = {'openid': '_openid', 'pwd': '_pwd'}
    __in_exclude__ = ['id', 'login_time', '_openid', 'user_id', 'base']
    __exclude__ = ['_openid']
    __permission__ = [need_json_exclude_get,
                      can_not_delete_this_rescources]
