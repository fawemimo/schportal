from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def validate_file_size(file):
    max_size_kb = 2000

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'File can not be larger than {max_size_kb}KB')


def email_validator(value):

    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError({"meesage":"Please enter a valid email address"})