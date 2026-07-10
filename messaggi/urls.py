from django.urls import path
from . import views

app_name = 'messaggi'

urlpatterns = [
    path('', views.lista_conversazioni_view, name='lista_conversazioni'),
    path('<str:username>/', views.conversazione_view, name='conversazione'),
]
