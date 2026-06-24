from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    autore         = models.ForeignKey(
        settings.AUTH_USER_MODEL,       # <-- mai importare CustomUser direttamente
        on_delete=models.CASCADE,
        related_name='posts',           # user.posts.all()
    )
    caption        = models.TextField(max_length=2200, blank=True)
    data_creazione = models.DateTimeField(default=timezone.now)
    aggiornato_il  = models.DateTimeField(auto_now=True)
    archiviato     = models.BooleanField(default=False)
    eliminato_da_moderatore = models.BooleanField(default=False)

    like       = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_con_like',  blank=True)
    salvati_da = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_salvati',   blank=True)

    class Meta:
        ordering = ['-data_creazione']

    @property
    def num_like(self):
        return self.like.count()

    @property
    def num_commenti(self):
        return self.commenti.filter(risposta_a__isnull=True).count()

    def __str__(self):
        return f"Post di {self.autore.username} — {self.data_creazione:%d/%m/%Y %H:%M}"


class MediaPost(models.Model):
    TIPO_CHOICES = (
        ('immagine', 'Immagine'),
        ('video',    'Video'),
    )
    post   = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file   = models.FileField(upload_to='posts/')
    tipo   = models.CharField(max_length=10, choices=TIPO_CHOICES, default='immagine')
    ordine = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordine']

    def __str__(self):
        return f"{self.tipo} #{self.ordine} — Post {self.post.id}"


class Hashtag(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    post = models.ManyToManyField(Post, related_name='hashtag', blank=True)

    def __str__(self):
        return f"#{self.nome}"


class Commento(models.Model):
    post           = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commenti')
    autore         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commenti')
    testo          = models.TextField(max_length=1000)
    data_creazione = models.DateTimeField(default=timezone.now)
    risposta_a     = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE, related_name='risposte',
    )
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='commenti_con_like', blank=True)

    class Meta:
        ordering = ['data_creazione']

    @property
    def num_like(self):
        return self.like.count()

    def __str__(self):
        return f"Commento di {self.autore.username} su Post {self.post.id}"


class Segnalazione(models.Model):
    MOTIVO_CHOICES = (
        ('spam',     'Spam'),
        ('odio',     "Incitamento all'odio"),
        ('violenza', 'Contenuto violento'),
        ('altro',    'Altro'),
    )
    STATO_CHOICES = (
        ('in_attesa', 'In attesa'),
        ('risolta',   'Risolta'),
        ('ignorata',  'Ignorata'),
    )
    segnalato_da  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='segnalazioni_inviate')
    post          = models.ForeignKey(Post,     null=True, blank=True, on_delete=models.CASCADE,  related_name='segnalazioni')
    commento      = models.ForeignKey(Commento, null=True, blank=True, on_delete=models.CASCADE,  related_name='segnalazioni')
    motivo        = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
    descrizione   = models.TextField(max_length=500, blank=True)
    stato         = models.CharField(max_length=20, choices=STATO_CHOICES, default='in_attesa')
    gestita_da    = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='segnalazioni_gestite'
    )
    creata_il     = models.DateTimeField(default=timezone.now)
    aggiornata_il = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creata_il']

    def __str__(self):
        return f"Segnalazione [{self.motivo}] da {self.segnalato_da.username} — {self.stato}"