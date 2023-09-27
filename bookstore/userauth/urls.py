from django.urls import path

from .views import UsersAuth

urlpatterns = [
    path("signup/", UsersAuth.as_view({'post': 'create'}), name="signup"),
    path("login/", UsersAuth.as_view({ 'get': 'retrieve'}), name="login")
    ]