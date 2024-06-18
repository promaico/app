from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _ 
from .managers import CustomUserManager
from django.contrib.auth.hashers import make_password


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("Benutzername"), max_length=100, unique=True)
    first_name = models.CharField(_("Vorname"), max_length=100)
    last_name = models.CharField(_("Nachname"), max_length=100)
    email = models.EmailField(_("E-Mail"), max_length=254, unique=True, null=False, blank=False)
    email_password = models.CharField(_("E-Mail Passwort"), max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email_password"]
    
    
    objects = CustomUserManager()

    def set_email_password(self, email_password):
        self.email_password = make_password(email_password)
        
        
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        
    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    