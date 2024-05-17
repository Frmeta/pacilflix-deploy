from authentication.views import login, profile
from django.urls import path
from main.views import *

urlpatterns = [
    # ariana
    # path("", home, name="home"),
    path("login/", login, name="login"),
    path("profile/", profile, name="profile"),
]
