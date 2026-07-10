from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Auth
    path('registrati/',             views.RegistrazioneView.as_view(), name='registrazione'),
    path('login/',                  views.login_view,                  name='login'),
    path('logout/',                 views.logout_view,                 name='logout'),

    # Profilo
    path('profilo/<str:username>/', views.profilo_view,                name='profilo'),
    path('impostazioni/',           views.modifica_profilo_view,       name='modifica_profilo'),

    # Follow
    path('follow/<str:username>/',          views.toggle_follow_view,      name='toggle_follow'),
    path('richiesta/<str:username>/',        views.gestisci_richiesta_view, name='gestisci_richiesta'),

    # Moderatore — utenti
    path('moderatore/utenti/',              views.lista_utenti_view,        name='lista_utenti'),
    path('moderatore/ban/<str:username>/',  views.ban_utente_view,          name='ban_utente'),
]
