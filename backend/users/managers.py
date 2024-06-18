from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Es muss eine E-Mail angegeben sein"))
        
        
    def create_user(self, username, first_name, last_name, email, password, email_password, **extra_fields):
        
        if not username:
            raise ValueError(_("Ein Benutzername ist erforderlich"))
        
        if not first_name:
            raise ValueError(_("Ein Vorname ist erforderlich"))
        
        if not last_name:
            raise ValueError(_("Ein Nachname ist erforderlich"))
        
        #if email:
        #    email = self.normalize_email(email)
        #    self.email_validator(email)
        #else:
        #    raise ValueError(_("Benutzer: Eine E-Mail Adresse ist erforderlich"))
        
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            **extra_fields
        )
        
        user.set_password(password)
        user.set_email_password(email_password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        user.save()
        
        return user
    
    def create_superuser(self, username, first_name, last_name, email, password, email_password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers müssen is_superuser=True haben"))
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superusers müssen is_staff=True haben"))
        
        if not password:
            raise ValueError(_("Superusers müssen ein Passwort besitzen"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Admin: Eine E-Mail Adresse ist erforderlich"))

        user = self.create_user(username, first_name, last_name, email, password, email_password, **extra_fields)
        user.save()
        
        return user