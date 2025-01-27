from django import forms
from utils.django_forms import add_placeholder, strong_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username'),
        add_placeholder(self.fields['email'], 'Your e-mail'),
        add_placeholder(self.fields['password'], 'Type your password'),
        add_placeholder(self.fields['password2'], 'Repeat your password'),
    username = forms.CharField(
        label='Username',
        error_messages={
            'required':'Write your username',
            'min_length':'Username must have at least 4 characters',
            'max_length':'Username must have less than 100 characters',
        },
        help_text='Username must have letters, numbers or one of those @.+-_. ',
        min_length=4, max_length=100
    )
    email = forms.EmailField(
        label='Email address',
        error_messages={'required': 'Write your email'},
        help_text='The e-mail must be valid',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required':'Write your password'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required':'Repeat your password'
        },
        label='Password Confirmation'
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
                'This email is already in use',
                  code='invalid'
            )
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password2 != password:
            password_error = ValidationError(
                ('The passwords must be equal'),
                code='invalid'
            )
            raise ValidationError({
                'password': password_error,
                'password2': password_error,
            })