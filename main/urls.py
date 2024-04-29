from django.urls import path
from main.views import *

urlpatterns = [
    path('kontributor/', kontributor, name='kontributor_page'),
    path('langganan/', langganan, name='langganan_page'),
    path('update_langganan/', update_langganan, name='update_langganan_page'),
]