from django import forms
from utils.django_forms import add_placeholder, strong_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu nome de usuário'),
        add_placeholder(self.fields['email'], 'Seu e-mail'),
        add_placeholder(self.fields['password'], 'Digite sua senha'),
        add_placeholder(self.fields['password2'], 'Repita sua senha'),
    username = forms.CharField(
        label='Nome de Usuário',
        error_messages={
            'required':'Escreva seu nome de usuário',
            'min_length':'Nome de Usuário deve possuir pelo menos 4 caracteres',
            'max_length':'Nome de Usuário deve possuir no máximo 100 caracteres',
        },
        help_text='Nome de Usuário deve ter letras, números ou algum desses símbolos @.+-_. ',
        min_length=4, max_length=100
    )
    email = forms.EmailField(
        label='Email',
        error_messages={'required': 'Escreva seu E-mail'},
        help_text='O e-mail deve ser válido',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required':'Escreva sua senha'
        },
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O tamanho deve ser de '
            'no mínimo 8 caracteres.'
        ),
        validators=[strong_password],
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required':'Repita sua senha'
        },
        label='Confirmar Senha'
    )
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]
    
    def clean_email(self):
        email = self.cleaned_data['email']
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                'Este e-mail já esta em uso.',
                  code='invalid'
            )
        return email
    def clean_username(self):
        username = self.cleaned_data['username']
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise ValidationError(
                'Este Nome de usuário já esta em uso.',
                  code='invalid'
            )
        return username
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password2 != password:
            password_error = ValidationError(
                ('As senhas precisam ser iguais.'),
                code='invalid'
            )
            raise ValidationError({
                'password': password_error,
                'password2': password_error,
            })