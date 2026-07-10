from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Feed (CBV)
    path('',                              views.FeedView.as_view(),               name='feed'),

    # CRUD post
    path('nuovo/',                        views.crea_post_view,                   name='crea_post'),
    path('<int:pk>/',                     views.dettaglio_post_view,              name='dettaglio'),
    path('<int:pk>/modifica/',            views.modifica_post_view,               name='modifica_post'),
    path('<int:pk>/elimina/',             views.elimina_post_view,                name='elimina_post'),

    # Like / salva
    path('<int:pk>/like/',                views.toggle_like_view,                 name='toggle_like'),
    path('<int:pk>/salva/',               views.toggle_salva_view,                name='toggle_salva'),

    # Commenti
    path('<int:pk>/commento/',            views.aggiungi_commento_view,           name='aggiungi_commento'),
    path('commento/<int:pk>/elimina/',    views.elimina_commento_view,            name='elimina_commento'),

    # Segnalazioni
    path('<int:pk>/segnala/',             views.segnala_post_view,                name='segnala_post'),

    # Moderatore — contenuti
    path('moderatore/',                   views.dashboard_moderatore_view,        name='dashboard_moderatore'),
    path('moderatore/seg/<int:pk>/',      views.gestisci_segnalazione_view,       name='gestisci_segnalazione'),
    path('moderatore/rimuovi/<int:pk>/',  views.elimina_post_moderatore_view,     name='elimina_post_moderatore'),
]