import re

from django.core.exceptions import ValidationError


def validate_phone(phone):
    pattern = r"[0-9]{14}"
    if not re.fullmatch(pattern, str(phone)):
        raise ValidationError("Formato de telefone inválido.")
    return phone
