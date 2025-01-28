from django import forms
from utils.django_forms import add_placeholder, add_attr
class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu nome de usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        self.fields['username'].label = 'Nome de Usuário'
        self.fields['password'].label = 'Senha'
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )