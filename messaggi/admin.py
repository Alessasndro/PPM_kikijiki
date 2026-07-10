from django.contrib import admin
from .models import Messaggio


@admin.register(Messaggio)
class MessaggioAdmin(admin.ModelAdmin):
    list_display  = ('mittente', 'destinatario', 'inviato_il', 'letto')
    list_filter   = ('letto',)
    search_fields = ('mittente__username', 'destinatario__username', 'testo')
