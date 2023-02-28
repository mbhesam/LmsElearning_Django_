from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
import os

def path_and_rename(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.pk, ext)
    return os.path.join(upload_to, filename)

class BaseUserManager(BUM):
    def create_user(self,email, is_active=True, is_admin=False, password=None):

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), is_active=is_active, is_admin=is_admin)

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
            is_active=True,
            is_admin=True,
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
        max_length=255,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )

    lastname = models.CharField(
        max_length=255,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )

    email = models.EmailField(verbose_name = "email address",
                              unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    grade_class = models.CharField(max_length=150)
    picture = models.ImageField(upload_to=path_and_rename,verbose_name="picture",blank=True) # upload_to=(instance,filename)
    type_user = models.CharField(max_length=10,choices=type_choices,default='student')
    objects = BaseUserManager()
    USERNAME_FIELD = "email"
    PASSWORD_FIELD = "password"
#    REQUIRED_FIELDS = ["username","password"]


    def __str__(self):
        return self.firstname+" "+self.lastname

    def is_staff(self):
        return self.is_admin