from django.core.management.base import BaseCommand, CommandError
from users.models import Profile
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext as _

def validate_password_strength(value):
    """Validates that a password is as least 7 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 7
    yes_or_no=input("do you want to bypass password complexity checking?[y/n]\t")
    if yes_or_no=='n':
        if len(value) < min_length:
            raise ValidationError(_('Password must be at least {0} characters '
                                    'long.').format(min_length))

        # check for digit
        if not any(char.isdigit() for char in value):
            raise ValidationError(_('Password must contain at least 1 digit.'))

        # check for letter
        if not any(char.isalpha() for char in value):
            raise ValidationError(_('Password must contain at least 1 letter.'))
    elif yes_or_no=='y':
        pass
    else:
        validate_password_strength(value)

class Command(BaseCommand):

    def handle(self, *args, **options):
        firstname = input("Enter firstname of admin:\t")
        lastname = input("Enter lastname of admin:\t")
        email = input("Enter email of admin:\t")
        password = input("Enter password of admin:\t")
        grade_class = "admin"
        type_user = "admin"
        try:
            validate_email(email)
        except ValidationError as e:
            print("not acceptable email, details:", e)
        validate_password_strength(password)
        object = Profile.objects.create(firstname=firstname,lastname=lastname,email=email,password=password,grade_class=grade_class,type_user=type_user,is_admin=True,is_active=True)
        object.save()
        print("admin user successfully created")
