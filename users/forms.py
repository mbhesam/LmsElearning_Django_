from django import forms
from django.forms import Textarea
from .models import Profile

class ProfileUser(forms.ModelForm):
    confirmpassword = forms.CharField(max_length=100)
    class Meta:
        model = Profile
        fields = ('firstname','lastname','email','password','confirmpassword','grade_class','picture','type_user')

    def is_valid(self):
        valid = super(ProfileUser,self).is_valid()
        if valid:
            if self.data['password'] == self.data['confirmpassword']:
                return True
            else:
                self.errors['password'] = 'does not match or it is blank'
                return False
        else:
            self.errors = "fields are not valid"
            return False

