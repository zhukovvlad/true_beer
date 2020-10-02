from django.core.exceptions import ValidationError

def validate_title(value):
    title = value
    if title.lower() == 'abc':
        raise ValidationError('Shut up you mother fucker!')
    return value