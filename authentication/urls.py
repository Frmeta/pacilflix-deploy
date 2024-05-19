from authentication.views import register, login, logout_user, show_main, show_register
from django.urls import path

urlpatterns = [
    # ariana
    path("", show_main, name="show_main"),
    path("register/", show_register, name="register"),
    path("handle-register/", register, name="handle_register"),
    path("login/", login, name="login"),
    path("logout/", logout_user, name="logout"),
]
