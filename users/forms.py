from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile

class UserRegisterForm(UserCreationForm):
    # default is required=ture if you want to make it optional required=false
    email = forms.EmailField()
    
    class Meta:
        model = User
        # model is with what you want the form (class) to interact with
        # here a new user will be created with every form
        fields = ['username', 'email', 'password1', 'password2'] 
        # the things( fields ) we wanna show in our form... password1 is the input password.. password2 is the confirmation password

class userUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class profileUpdateForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image']