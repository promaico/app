from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _ 
from .forms import CustomUserChangeForm, RegistrationForm
from .models import User

# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ["username"]
    add_form = RegistrationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["username", "first_name", "last_name", "email", "email_password"]
    list_display_links = ["username"]
    search_fields = ["username", "first_name", "last_name", "email"]
    readonly_fields = ["date_joined"]
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": ("username","password",)
            },
        ),
        (
            _("Personal Information"),
            {
                "fields": ("first_name", "last_name", "email", "email_password")
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
            },
        ),
        (
            _("Important Dates"),
            {
                "fields": ("last_login", "date_joined")
            }
        )
    )
    
    
admin.site.register(User, UserAdmin)