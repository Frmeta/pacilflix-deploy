from django.urls import path
from main.views import *

urlpatterns = [
    path('film/', hal_film_page, name='hal_film_page'),
    path('series/', hal_series_page, name='hal_series_page'),
    path('episode/', hal_episode_page, name='hal_episode_page'),
    path('ulasan/', ulasan_page, name='ulasan_page'),
]