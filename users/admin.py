from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ('username', 'email', 'ruolo', 'is_banned', 'is_active', 'date_joined')
    list_filter   = ('ruolo', 'is_banned', 'is_active', 'account_privato')
    search_fields = ('username', 'email')
    actions       = ['banna_utenti', 'sbanna_utenti']

    fieldsets = UserAdmin.fieldsets + (
        ('Profilo Social', {
            'fields': ('ruolo', 'immagine_profilo', 'bio', 'link_sito', 'data_nascita', 'account_privato', 'is_banned')
        }),
    )

    def banna_utenti(self, request, queryset):
        queryset.update(is_banned=True)
    banna_utenti.short_description = "Banna utenti selezionati"

    def sbanna_utenti(self, request, queryset):
        queryset.update(is_banned=False)
    sbanna_utenti.short_description = "Sbanna utenti selezionati"