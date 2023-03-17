from users.models import Profile
from django.contrib.auth.backends import ModelBackend
class EmailBackend(ModelBackend):
    @staticmethod
    def authenticate(request, username=None, password=None, **kwargs):
        try:
            user = Profile.objects.get(email=username)
        except Profile.DoesNotExist:
            return None
        else:
            if user.password == password:
                return user
        return None
