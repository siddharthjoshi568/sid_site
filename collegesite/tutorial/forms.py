from django import forms
from django.forms import ModelForm
from tutorial.models import Comment,Reply,Student_Model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    name = forms.CharField()
    computer_code = forms.CharField()
    course = forms.CharField()
    class Meta:
        model = User
        fields = ['username','name','email','computer_code','course','password1','password2']

class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Student_Model
        fields = ['name','computer_code','image','enrollment_no','course']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())