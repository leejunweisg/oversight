from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    # adds an email field on top of the fields in UserCreationForm
    email = forms.EmailField() # default required=True
    
    # defines which model this form is linked to
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() # default required=True
    
    # defines which model this form is linked to
    class Meta:
        model = User
        fields = ['username', 'email']
