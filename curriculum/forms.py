from django import forms
from .models import Topics,Comment,Reply
class Topic_Form(forms.ModelForm):
    class Meta:
        model = Topics
        fields = ["name","chapter","video","ppt","notes"]
class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body":"Comment:"}
        widgets = {
            "body" : forms.Textarea(attrs={'class':'form-control' , 'rows':4,'cols':70,'placeholder':"Enter Your Comment"})
        }

class Reply_Form(forms.ModelForm):
    class Meta :
        model = Reply
        fields = ['body']
        widgets = {
        "body": forms.Textarea(
            attrs={'class': 'form-control', 'rows': 2, 'cols': 10})}




