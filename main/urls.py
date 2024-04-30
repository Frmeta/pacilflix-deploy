from django.urls import path
from main.views import *

urlpatterns = [
    path('kontributor/', kontributor, name='kontributor_page'),
    path('kontributor_pemain/', kontributor_pemain, name='kontributor_pemain_page'),
    path('kontributor_sutradara/', kontributor_sutradara, name='kontributor_sutradara_page'),
    path('kontributor_penulis_skenario/', kontributor_penulis_skenario, name='kontributor_penulis_skenario_page'),
    path('langganan/', langganan, name='langganan_page'),
    path('update_langganan/', update_langganan, name='update_langganan_page'),
]