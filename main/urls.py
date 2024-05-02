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

    # fredo
    path('daftar_unduhan/', daftar_unduhan, name='daftar_unduhan'),
    path('daftar_favorit/', daftar_favorit, name='daftar_favorit'),

    # ariana
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
]