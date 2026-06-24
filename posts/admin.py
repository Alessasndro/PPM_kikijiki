from django.contrib import admin
from .models import Post, MediaPost, Hashtag, Commento, Segnalazione


class MediaPostInline(admin.TabularInline):
    model = MediaPost
    extra = 1


class CommentoInline(admin.TabularInline):
    model = Commento
    extra = 0
    readonly_fields = ('autore', 'testo', 'data_creazione')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('autore', 'data_creazione', 'num_like', 'archiviato', 'eliminato_da_moderatore')
    list_filter   = ('archiviato', 'eliminato_da_moderatore')
    search_fields = ('autore__username', 'caption')
    inlines       = [MediaPostInline, CommentoInline]
    actions       = ['rimuovi_post']

    def rimuovi_post(self, request, queryset):
        queryset.update(eliminato_da_moderatore=True)
    rimuovi_post.short_description = "Rimuovi post selezionati (soft delete)"


@admin.register(Commento)
class CommentoAdmin(admin.ModelAdmin):
    list_display  = ('autore', 'post', 'data_creazione', 'risposta_a')
    search_fields = ('autore__username', 'testo')


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    search_fields = ('nome',)


@admin.register(Segnalazione)
class SegnalazioneAdmin(admin.ModelAdmin):
    list_display  = ('segnalato_da', 'motivo', 'stato', 'gestita_da', 'creata_il')
    list_filter   = ('stato', 'motivo')
    search_fields = ('segnalato_da__username',)
    actions       = ['segna_risolta', 'segna_ignorata']

    def segna_risolta(self, request, queryset):
        queryset.update(stato='risolta', gestita_da=request.user)
    segna_risolta.short_description = "Segna come risolta"

    def segna_ignorata(self, request, queryset):
        queryset.update(stato='ignorata', gestita_da=request.user)
    segna_ignorata.short_description = "Segna come ignorata"