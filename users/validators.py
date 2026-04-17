# users/validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UppercaseValidator:
    """Vérifie que le mot de passe contient au moins une majuscule"""
    
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une majuscule (A-Z)."),
                code='password_no_upper',
            )
    
    def get_help_text(self):
        return _("Votre mot de passe doit contenir au moins une majuscule (A-Z).")


class SpecialCharacterValidator:
    """Vérifie que le mot de passe contient au moins un caractère spécial"""
    
    def validate(self, password, user=None):
        # Caractères spéciaux courants
        special_chars = r'[!@#$%^&*(),.?":{}|<>]'
        if not re.findall(special_chars, password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&* etc.)."),
                code='password_no_special',
            )
    
    def get_help_text(self):
        return _("Votre mot de passe doit contenir au moins un caractère spécial (!@#$%^&* etc.).")


class NumberValidator:
    """Vérifie que le mot de passe contient au moins un chiffre"""
    
    def validate(self, password, user=None):
        if not re.findall('[0-9]', password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un chiffre (0-9)."),
                code='password_no_number',
            )
    
    def get_help_text(self):
        return _("Votre mot de passe doit contenir au moins un chiffre (0-9).")