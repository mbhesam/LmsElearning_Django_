from django.contrib.auth.hashers import check_password
#from django.contrib.auth.models import User
from users.models import Profile

class EmailAuthBackend:
    """
    Custom authentication backend.

    Allows users to log in using their email address.
    """

    def authenticate(self, request, email=None, password=None):
        """
        Overrides the authenticate method to allow users to log in using their email address.
        """
        try:
            user = Profile.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Overrides the get_user method to allow users to log in using their email address.
        """
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None
