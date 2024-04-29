from django.urls import path
from main.views import *

urlpatterns = [
    path('kontributor/', kontributor_page, name='kontributor_page'),
    path('langganan/', langganan_page, name='langganan_page'),
    path('update-langganan/', update_langganan_page, name='update_langganan_page'),
]