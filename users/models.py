from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin

class BaseUserManager(BUM):
    def create_user(self,email, password=None):

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()))

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self,email, password=None):

        user = self.create_user(
            email=email,
            password=password,
        )
        user.save(using=self._db)

        return user

class Profile(AbstractBaseUser):
    type_choices= (
                      ('admin','admin'),
                      ('student','student'),
                      ('teacher','teacher'),
                      ('parent','parent'),
    )
    firstname = models.CharField(
        max_length=255
    )

    lastname = models.CharField(
        max_length=255,
    )

    email = models.EmailField(verbose_name = "email address",
                              unique=True)
    password = models.CharField(max_length=100)
    grade_class = models.CharField(max_length=150)
    picture = models.ImageField(upload_to="user",verbose_name="picture",default='Lionel-Messi-11.jpg') # upload_to=(instance,filename)
    type_user = models.CharField(max_length=10,choices=type_choices,default='student')
    objects = BaseUserManager()
    USERNAME_FIELD = "email"
    PASSWORD_FIELD = "password"
#    REQUIRED_FIELDS = ["username","password"]


    def __str__(self):
        return self.lastname

    def is_staff(self):
        return self.type_user
