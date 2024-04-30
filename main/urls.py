from django.urls import path
from main.views import *

urlpatterns = [
    path('tayangan_guest/', tayangan_guest, name='tayangan_guest_page'),
    path('hasil_pencarian_guest/', hasil_pencarian_guest, name='hasil_pencarian_guest_page'),
    path('tayangan_aktif/', tayangan_aktif, name='tayangan_aktif_page'),
    path('hasil_pencarian_aktif/', hasil_pencarian_aktif, name='hasil_pencarian_aktif_page'),
    path('film/', hal_film_page, name='hal_film_page'),
    path('series/', hal_series_page, name='hal_series_page'),
    path('episode/', hal_episode_page, name='hal_episode_page'),
    path('ulasan/', ulasan_page, name='ulasan_page'),
]