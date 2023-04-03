from django.contrib.auth.backends import BaseBackend


class AdminBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        pass

    def get_user(self, user_id):
        pass

    def has_perm(self, user_obj, perm, obj=None):
        return \
            user_obj.is_active and \
            (user_obj.is_staff or user_obj.is_superuser) and \
            super().has_perm(user_obj, perm, obj=obj)
