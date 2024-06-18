from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/register/', views.RegistrationView, name="register"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/profile/', views.profile_view, name="profile" ),
    path('accounts/profile/email/', views.email_view, name="email")
]
