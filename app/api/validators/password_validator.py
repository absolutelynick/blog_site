import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator(object):
    def __init__(self, min_digits=0):
        self.min_digits = min_digits
        self.help_text = _(f"The password must contain {self.min_digits} digits, 0-9.")

    def validate(self, password, user=None):
        if not len(re.findall("\d", password)) >= self.min_digits:
            raise ValidationError(self.help_text, code="password_no_number")

    def get_help_text(self):
        return self.help_text


class UppercaseValidator(object):
    def __init__(self, min_digits=0):
        self.min_digits = min_digits
        self.help_text = _(
            f"The password must contain {self.min_digits} uppercase letters, A-Z."
        )

    def validate(self, password, user=None):
        if not len(re.findall("[A-Z]", password)) >= self.min_digits:
            raise ValidationError(self.help_text, code="password_no_upper")

    def get_help_text(self):
        return self.help_text


class LowercaseValidator(object):
    def __init__(self, min_digits=0):
        self.min_digits = min_digits
        self.help_text = _(
            f"The password must contain {self.min_digits} lowercase letters, a-z."
        )

    def validate(self, password, user=None):
        if not len(re.findall("[a-z]", password)) >= self.min_digits:
            raise ValidationError(self.help_text, code="password_no_lower")

    def get_help_text(self):
        return self.help_text


class SymbolValidator(object):
    symbols = "[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]"

    def __init__(self, min_digits=0):
        self.min_digits = min_digits
        self.help_text = _(
            f"The password must contain {self.min_digits} symbols: {self.symbols}"
        )

    def validate(self, password, user=None):
        if not len(re.findall(self.symbols, password)) >= self.min_digits:
            raise ValidationError(
                _(
                    f"The password must contain {self.min_digits} symbol in: {self.symbols}"
                ),
                code="password_no_symbol",
            )

    def get_help_text(self):
        return self.help_text
