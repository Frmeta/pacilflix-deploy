from django.urls import path
from main.views import *

urlpatterns = [
    # vanya
    path('tayangan_guest/', tayangan_guest, name='tayangan_guest_page'),
    path('hasil_pencarian_guest/', hasil_pencarian_guest, name='hasil_pencarian_guest_page'),
    path('tayangan_aktif/', tayangan_aktif, name='tayangan_aktif_page'),
    path('hasil_pencarian_aktif/', hasil_pencarian_aktif, name='hasil_pencarian_aktif_page'),
    path('detail/<str:id>/', detail_page, name='detail_page'),
    path('episode/<str:title>/<str:id>/', episode_page, name='episode_page'),
    path('watch/<str:id>/', watch, name='watch'),
    path('review/<str:id>/', review, name='review'),

    # fredo
    path('daftar_unduhan/', daftar_unduhan, name='daftar_unduhan'),
    path('unduh/', unduh, name='unduh'),
    path('hapus_unduhan/', hapus_unduhan, name='hapus_unduhan'),
    
    path('daftar_favorit/', daftar_favorit, name='daftar_favorit'),
    path("bikin_daftar_favorit", bikin_daftar_favorit, name='bikin_daftar_favorit'),
    path("get_daftar_favorit/", get_daftar_favorit, name="get_daftar_favorit"),

    path('tambah_favorit/', tambah_favorit, name='tambah_favorit'),
    path('detail_daftar_favorit/', detail_daftar_favorit, name='detail_daftar_favorit'),


    # sabina
    path("kontributor/", kontributor, name="kontributor_page"),
    path("kontributor_pemain/", kontributor_pemain, name="kontributor_pemain_page"),
    path(
        "kontributor_sutradara/",
        kontributor_sutradara,
        name="kontributor_sutradara_page",
    ),
    path(
        "kontributor_penulis_skenario/",
        kontributor_penulis_skenario,
        name="kontributor_penulis_skenario_page",
    ),
    path("langganan/", langganan, name="langganan_page"),
    path("update_langganan/", update_langganan, name="update_langganan_page"),
]
