from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
#from mongoengine import Document, fields
class User(AbstractBaseUser):
    email = models.EmailField(("email address"), blank=True)
    objects = UserManager()

    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_email(self):
        """Return the short name for the user."""
        return self.email




