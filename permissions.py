#coding:utf-8
class Base():
    """基本权限类，不提供任何权限逻辑"""
    def get(self, db_session, object, request, pk):
        "基本get权限"
        return True

    def put(self, db_session, object, request, pk):
        "基本put权限"
        return True

    def post(self, db_session, object, request):
        "基本post权限"
        return True

    def delete(self, db_session, object, request, pk):
        "基本delete权限"
        return True


class test_permission(Base):
    """测试权限，只开放get接口"""

    def get(self, db_session, object, request, pk):
        "无 get 权限"
        return True

    def put(self, db_session, object, request, pk):
        "无 put 权限"
        return False

    def post(self, db_session, object, request):
        "无 post 权限"
        return False

    def delete(self, db_session, object, request, pk):
        "无 delete 权限"
        return False
