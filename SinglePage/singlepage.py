# coding: utf-8
from flask import *
from flask.views import *
from serializer import *
import inspect
import sys

app = Flask(__name__)
app.config['resources'] = {}


def register(cls, endpoint=''):
    endpoint = endpoint
    view = cls.as_view(cls.__name__)
    cls.pk_list = {}
    resource_name = endpoint
    app.config['resources'].update({resource_name: cls})
    for method in cls.methods:  
        lowcase_method = method.lower()
        try:
            func = getattr(cls, lowcase_method)
        except AttributeError, e:
            pass
        args = []
        defaults = []
        if inspect.getargspec(func)[0] is not None:
            args = [e for e in inspect.getargspec(
                func)[0] if e is not 'self']

        if inspect.getargspec(func)[3] is not None:
            defaults = [e for e in inspect.getargspec(
                func)[3] if e is not 'self']
        defaults_dict = dict([(arg, default)
                              for arg in args for default in defaults])
        for arg in args:
            cls.pk_list.update({lowcase_method: arg})
            app.add_url_rule(endpoint + '<' + arg + '>',
                             view_func=view, defaults=defaults_dict, methods=[method, ])
    cls.object = cls
    app.add_url_rule(endpoint, view_func=view)


class SinglePage(View):
    """this is the base class of single page"""
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def create_object(self, json=None):
        if json is not None:
            class_dict = serializer.attr_dict_from_sqlalchemy_in_exclude(self)
            for item in class_dict:
                setattr(self, item, json[item])
        return self

    def dispatch_request(self, *args, **kwargs):
        if request.method == 'GET':
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['get']: None}
                except KeyError, e:
                    pass
            response, class_type = self.get(*args, **kwargs)
            if class_type == 'origin':
                return response
            def generator():
                yield '{"data":['
                for r in response.yield_per(1):
                    data = serializer.dump(r)
                    yield json.dumps(data)+','
                yield '{}]}'
            return Response(generator(),200,{'Content-type':'application/json'})
        elif request.method == 'POST':
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['post']: None}
                except KeyError, e:
                    pass
            response, class_type = self.post(*args, **kwargs)
            if class_type == 'origin':
                return response
            return jsonify({'data': serializer.dump(response, class_type)})
        elif request.method == 'PUT':
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['put']: None}
                except KeyError, e:
                    pass
            response, class_type = self.put(*args, **kwargs)
            if class_type == 'origin':
                return response
            return jsonify({'data': serializer.dump(response, class_type)})
        elif request.method == 'DELETE':
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['delete']: None}
                except KeyError, e:
                    pass
            response, class_type = self.delete(*args, **kwargs)
            if class_type == 'origin':
                return response
            return jsonify({'data': serializer.dump(response, class_type)})


class permission():

    def get(self, db_session, cls, request, pk):
        'get permission'
        return True

    def post(self, db_session, cls, request):
        'post permission'
        return True

    def put(self, db_session, cls, request, pk):
        'put permission'
        return True

    def delete(self, db_session, cls, request, pk):
        'delete permission'
        return True


class GeneralViewWithSQLAlchemy(SinglePage):
    """docstring for GeneralView"""
    db_session = None
    real_delete = True

    # 处理http get方法

    def filter(query, value):
        """
        等于 key = value
        不等于 key != value
        boolean 值 Flase：0，True：1
        大于 key > value
        小于 key < value
        或 expression A or expression B
        且 expression A and expression B
            ex:
                'name = taylor and and age <20 and deleted = 0'
        """
        from sqlalchemy import text

        return query.filter(text(value))

    def asc_order_by(query, value):
        from sqlalchemy import text

        return query.order_by(text(value))

    def desc_order_by(query, value):
        from sqlalchemy import desc
        from sqlalchemy import text

        return query.order_by(desc(text(value)))

    def limit(query, value):
        return query[0:int(value)]

    def fileds(query, value):
        pass

    # 过滤器实现于args名称字典
    __in_exclude__ = []
    # 定义哪些字段不展示给前端
    __exclude__ = []
    # 定义属性装饰方法
    __property__ = {}
    __permission__ = [permission]
    __query_args__ = {'filter': filter, 'asc_order_by': asc_order_by,
                      'desc_order_by': desc_order_by, 'limit': limit, 'fileds': fileds}

    def get_permission_passed(self, pk):
        for permission in self.__permission__:
            if not permission().get(self.db_session, self.object, request, pk):
                return False, permission
        return True, None

    def put_permission_passed(self, pk):
        for permission in self.__permission__:
            if not permission().put(self.db_session, self.object, request, pk):
                return False, permission
        return True, None

    def post_permission_passed(self):
        for permission in self.__permission__:
            if not permission().post(self.db_session, self.object, request):
                return False, permission
        return True, None

    def delete_permission_passed(self, pk):
        for permission in self.__permission__:
            if not permission().delete(self.db_session, self.object, request, pk):
                return False, permission
        return True, None

    def get_hook_on_get_query(self,query):
        return query

    def get(self, pk):
        '获取资源列表或资源'
        # 查询数据
        passed, permission = self.get_permission_passed(pk)
        if not passed:
            return ("permission hint: " + permission().get.__doc__, 401), 'origin'
        if pk is not None:
            query = self.db_session.query(
                self.object).filter(self.object.id == pk)
            query = self.get_hook_on_get_query(query)
            return query, 'sqlalchemy'
        else:
            import time
            start = time.time()
            query = self.db_session.query(self.object)
            end = time.time()
            print 'origin query:'+str(end-start)
            start = time.time()
            for arg in self.__query_args__:
                value = request.args.get(arg, None)
                if value is not None:
                    query = self.__query_args__[arg](query, value)
            query = self.get_hook_on_get_query(query)
            end = time.time()
            print 'args query:'+str(end-start)
            return query, 'sqlalchemy'
    # 处理http post方法
    def post_hook_before_create_object(self,data):
        return data

    def post(self):
        '新建该资源'
        # 获取request的json并新建一个用户
        passed, permission = self.post_permission_passed()
        if not passed:
            return ("permission hint: " + permission().post.__doc__, 401), 'origin'
        class_dict = serializer.attr_dict_from_sqlalchemy_in_exclude(self)
        data = request.get_json()
        if data is not None:
            try:
                for key in class_dict:
                    value = data[key]
            except KeyError, e:
                return ('if you want to create a new resources, you need thoese keywords: ' + ' ,'.join(class_dict), 401), 'origin'
        data = self.post_hook_before_create_object(data)
        obj = super(GeneralViewWithSQLAlchemy,self).create_object(data)
        self.db_session.add(obj)
        self.db_session.commit()
        return obj, 'sqlalchemy'

    def delete(self, pk):
        '删除一个资源'
        passed, permission = self.delete_permission_passed(pk)
        if not passed:
            return ("permission hint: " + permission().delete.__doc__, 401), 'origin'
        if self.real_delete:
            if pk is not None:
                self.db_session.query(self.object).filter(
                    self.object.id == pk).delete()
                self.db_session.commit()
                return self.db_session.query(self.object).filter(
                    self.object.id == pk), 'sqlalchemy'
            else:
                return 'need pk', 'basic'
        else:
            if pk is not None:
                self.db_session.query(self.object).filter(
                    self.object.id == pk).update({self.object.deleted: True})
                self.db_session.commit()
                return self.db_session.query(self.object).filter(
                    self.object.id == pk), 'sqlalchemy'
            else:
                return 'need pk', 'basic'

    def put(self, pk):
        '更新一个资源'
        passed, permission = self.put_permission_passed(pk)
        if not passed:
            return ("permission hint: " + permission().put.__doc__, 401), 'origin'
        if pk is not None:
            query = self.db_session.query(self.object).filter(
                self.object.id == pk)
            self = query.first()
            data = request.get_json()
            properties = [d for d in data if d in self.__property__]
            for d in properties:
                setattr(self, d, data[d])
                value = getattr(self, d)
                del data[d]
                data[self.__property__[d]] = value
            if data != {}:
                query.update(data)
            self.db_session.commit()
            return self.db_session.query(self.object).filter(
                self.object.id == pk), 'sqlalchemy'
        else:
            return 'need pk', 'basic'

        