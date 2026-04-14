import re

from django.core.exceptions import ValidationError


def validate_phone(phone):
    pattern = r"[0-9]{13}"
    if not re.fullmatch(pattern, str(phone)):
        raise ValidationError("Formato de telefone inválido.")
    return phone


def normalize_contact(contact):
    digits = "".join(filter(str.isdigit, str(contact or "")))

    if len(digits) == 11:
        return digits
    print(f"DEBUG DIGITIS >>> {len(digits)}")
    return None
