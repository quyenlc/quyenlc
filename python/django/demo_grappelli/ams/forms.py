from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username',}))
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password',}))
    def login(self):
        if self.is_valid():            
            fields = self.cleaned_data
            user = authenticate(username=fields['username'], password=fields['password'])
            return user
        else:
            return None