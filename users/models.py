from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('standard',  'Utente Standard'),
        ('moderator', 'Moderatore'),
    )
    ruolo = models.CharField(max_length=20, choices=ROLE_CHOICES, default='standard')

    # --- PROFILO ---
    immagine_profilo = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio              = models.TextField(max_length=500, blank=True)
    link_sito        = models.URLField(max_length=200, blank=True)
    data_nascita     = models.DateField(null=True, blank=True)
    account_privato  = models.BooleanField(default=False)
    is_banned        = models.BooleanField(default=False)   # gestito dal moderatore

    # --- FOLLOW ---
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
    )
    richieste_follow = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='richieste_in_arrivo',
        blank=True,
    )

    # --- PROPERTIES ---
    @property
    def num_followers(self):
        return self.followers.count()

    @property
    def num_following(self):
        return self.following.count()

    @property
    def num_post(self):
        # related_name='posts' definito in Post.autore
        return self.posts.filter(archiviato=False, eliminato_da_moderatore=False).count()

    @property
    def is_moderator(self):
        return self.ruolo == 'moderator'

    def __str__(self):
        return self.username