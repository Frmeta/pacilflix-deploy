from authentication.views import register, login, logout_user, show_main, register_page
from django.urls import path
from main.views import *

urlpatterns = [
    # ariana
    # path("", home, name="home"),
    # path("login/", login, name="login"),
    # path("profile/", profile, name="profile"),
    # path("", show_main, name="show_main"),
    # path("register/", register, name="register"),
    # path("login/", login, name="login"),
    # path("logout/", logout_user, name="logout"),
    path("", show_main, name="show_main"),
    path("register/", register_page, name="register"),
    path("handle-register/", register, name="handle_register"),
    path("login/", login, name="login"),
    path("logout/", logout_user, name="logout"),
]
