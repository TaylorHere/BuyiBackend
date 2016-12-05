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

