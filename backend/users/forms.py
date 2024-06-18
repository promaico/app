from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from .models import User
from django.core.exceptions import ValidationError
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["username", "first_name", "last_name", "email", "email_password", "password1", "password2"]
        error_class = "error"
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Es existiert bereits ein Account mit dieser E-Mail Adresse")
        return email
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ["username", "first_name", "last_name", "email", "email_password"]
        error_class = "error"
        
        
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]  
        
class Email_Form:
    sender = forms.EmailField(max_length=50, required=True)
    class Meta:
        fields = ["sender"]