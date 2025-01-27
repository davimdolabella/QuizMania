from django.core.exceptions import ValidationError
import re
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()
def add_placeholder(field, placeholder):
    add_attr(field, 'placeholder', placeholder)
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O tamanho deve ser de '
            'no mínimo 8 caracteres.'
        ), 
            code='invalid'
        )