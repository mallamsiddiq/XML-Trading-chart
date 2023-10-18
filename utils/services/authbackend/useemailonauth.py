from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None  # No user found with this email

        if user.check_password(password):
            return user  # User authenticated successfully

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        
class EmailBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, is_staff = None):
        UserModel = get_user_model()
        
        try:
            user = UserModel.objects.get(email = username)
            if user.check_password(password):
                if is_staff is not None:
                    if user.is_staff == is_staff:
                        return user
                    else:
                        return None
                return user

        except UserModel.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None