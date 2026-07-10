from django.db import models
from django.conf import settings
from django.utils import timezone


class Messaggio(models.Model):
    mittente     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messaggi_inviati',
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messaggi_ricevuti',
    )
    testo        = models.TextField(max_length=2000)
    inviato_il   = models.DateTimeField(default=timezone.now)
    letto        = models.BooleanField(default=False)

    class Meta:
        ordering = ['inviato_il']

    def __str__(self):
        return f"{self.mittente.username} → {self.destinatario.username}: {self.testo[:30]}"
