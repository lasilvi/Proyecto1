from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    def _init_(self, *args, **kwargs):
        super(UserLoginForm, self)._init_(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Correo electrónico','autocomplete': 'off'}),
        label="Correo electrónico")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':' form-control', 'placeholder': 'Contraseña','autocomplete': 'off'}),
         label="Contraseña")