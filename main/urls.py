from django.urls import path
from main.views import *

urlpatterns = [
    # vanya
    path('', tayangan_guest, name='tayangan_guest_page'),
    path('hasil_pencarian_guest/', hasil_pencarian_guest, name='hasil_pencarian_guest_page'),
    path('tayangan_aktif/', tayangan_aktif, name='tayangan_aktif_page'),
    path('hasil_pencarian_aktif/', hasil_pencarian_aktif, name='hasil_pencarian_aktif_page'),
    path('film/', hal_film_page, name='hal_film_page'),
    path('series/', hal_series_page, name='hal_series_page'),
    path('episode/', hal_episode_page, name='hal_episode_page'),

    # fredo
    path('daftar_unduhan/', daftar_unduhan, name='daftar_unduhan'),
    path('daftar_favorit/', daftar_favorit, name='daftar_favorit'),

    # sabina
    path('kontributor/', kontributor, name='kontributor_page'),
    path('kontributor_pemain/', kontributor_pemain, name='kontributor_pemain_page'),
    path('kontributor_sutradara/', kontributor_sutradara, name='kontributor_sutradara_page'),
    path('kontributor_penulis_skenario/', kontributor_penulis_skenario, name='kontributor_penulis_skenario_page'),
    path('langganan/', langganan, name='langganan_page'),
    path('update_langganan/', update_langganan, name='update_langganan_page'),
]