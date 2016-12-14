from SinglePage.singlepage import GeneralViewWithSQLAlchemy, request
from Model.User import User


class Dynamic_permission(GeneralViewWithSQLAlchemy):
    """docstring for Dynamic_permission"""

    def get_permission_passed(self, pk):
        super(Dynamic_permission, self).get_permission_passed(pk)
        user_id = request.headers.get('XXX-user-id', None)
        user = self.db_session.query(User).filter(User.id == user_id).first()
        permissions = user.permissions
        for permission in permissions:
            import permissions
            permission = getattr(permissions, permission.name, None)
            if not permission().get(self.db_session, self.object, request, pk):
                return False, permission
        return True, None

    def put_permission_passed(self, pk):
        super(Dynamic_permission, self).put_permission_passed(pk)
        user_id = request.headers.get('XXX-user-id', None)
        user = self.db_session.query(User).filter(User.id == user_id).first()
        permissions = user.permissions
        for permission in permissions:
            import permissions
            permission = getattr(permissions, permission.name, None)
            if not permission().put(self.db_session, self.object, request, pk):
                return False, permission
        return True, None

    def post_permission_passed(self):
        super(Dynamic_permission, self).post_permission_passed()
        user_id = request.headers.get('XXX-user-id', None)
        user = self.db_session.query(User).filter(User.id == user_id).first()
        permissions = user.permissions
        for permission in permissions:
            import permissions
            permission = getattr(permissions, permission.name, None)
            if not permission().post(self.db_session, self.object, request):
                return False, permission
        return True, None

    def delete_permission_passed(self, pk):
        super(Dynamic_permission, self).delete_permission_passed(pk)
        user_id = request.headers.get('XXX-user-id', None)
        user = self.db_session.query(User).filter(User.id == user_id).first()
        permissions = user.permissions
        for permission in permissions:
            import permissions
            permission = getattr(permissions, permission.name, None)
            if not permission().delete(self.db_session, self.object, request, pk):
                return False, permission
        return True, None
