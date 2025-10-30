from django.core.exceptions import ValidationError


def normalize_phone_number(phone_number):
    """Normalize Iranian mobile numbers to standard 09xxxxxxxxx format."""
    phone_number = phone_number.strip().replace(' ', '').replace('-', '')
    if phone_number.startswith('+98'):
        phone_number = '0' + phone_number[3:]
    elif phone_number.startswith('98'):
        phone_number = '0' + phone_number[2:]
    elif phone_number.startswith('9') and len(phone_number) == 10:
        phone_number = '0' + phone_number
    return phone_number


def validate_phone_number(value):
    normalized = normalize_phone_number(value)
    if not normalized.isdigit():
        raise ValidationError('شماره همراه باید فقط شامل اعداد باشد.')
    if len(normalized) != 11:
        raise ValidationError('شماره همراه باید 11 رقم باشد.')
    if not normalized.startswith('09'):
        raise ValidationError('شماره همراه باید با 09 شروع شود.')