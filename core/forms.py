from django.contrib.auth.models import User
from django import forms

#where the parameters for creating a new user object is stored. this is also used to create
#the register page.
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.CharField(label='Email',widget=forms.TextInput(attrs={'placeholder':'Email'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
