from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import assets

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

# Register/Create a User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Login a User

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

# Create-Assets
class CreateAssetForm(forms.ModelForm):
    class Meta:
        model = assets
        fields = ['asset_no','asset_name','brand','model','serial_no','department_name','owner_name','location','status','remark']

# Update-Assets
class UpdateAssetForm(forms.ModelForm):
    class Meta:
        model = assets
        fields = ['asset_no','asset_name','brand','model','serial_no','department_name','owner_name','location','status','remark']


    