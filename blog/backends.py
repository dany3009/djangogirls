from django.contrib.auth import get_user_model


User = get_user_model()


class EmailModelBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.filter(**kwargs).first()
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.filter(pk=user_id).first()
        except User.DoesNotExist:
            return None
