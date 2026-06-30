"""
Script per popolare il database con dati demo realistici.
Esegui con:
    python manage.py shell < populate_db.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, Commento, Segnalazione

User = get_user_model()

print("🗑️  Pulizia database...")
Segnalazione.objects.all().delete()
Commento.objects.all().delete()
Post.objects.all().delete()
User.objects.all().delete()

print("👤 Creazione utenti demo...")

# Superuser / admin (Kiki-Jiki)
admin = User.objects.create_superuser(
    username='kikijiki',
    email='admin@demo.it',
    password='admin12345',
    ruolo='moderator',
    bio='Il grande spaccaspecchi. Amministratore supremo della piattaforma 🔥',
)

# Moderatore
moderatore = User.objects.create_user(
    username='moderatore_demo',
    email='moderatore@demo.it',
    password='moderatore12345',
    ruolo='moderator',
    bio='Sono un moderatore. Tengo la community pulita.',
    link_sito='https://example.com',
)

# Utenti standard
user1 = User.objects.create_user(
    username='mario_rossi',
    email='mario@demo.it',
    password='user12345',
    ruolo='standard',
    first_name='Mario',
    last_name='Rossi',
    bio='Fotografo amatoriale 📷 | Milano',
    link_sito='https://mariorossi.it',
)

user2 = User.objects.create_user(
    username='giulia_bianchi',
    email='giulia@demo.it',
    password='user12345',
    ruolo='standard',
    first_name='Giulia',
    last_name='Bianchi',
    bio='Viaggiatrice seriale ✈️ | Food lover 🍕',
)

user3 = User.objects.create_user(
    username='luca_verdi',
    email='luca@demo.it',
    password='user12345',
    ruolo='standard',
    first_name='Luca',
    last_name='Verdi',
    bio='Dev di giorno, gamer di notte 🎮',
    account_privato=True,
)

user4 = User.objects.create_user(
    username='sara_neri',
    email='sara@demo.it',
    password='user12345',
    ruolo='standard',
    first_name='Sara',
    last_name='Neri',
    bio='Artista digitale 🎨 | Torino',
)

print("🤝 Creazione relazioni follow...")

user1.following.add(user2, user4)
user2.following.add(user1, user3)
user4.following.add(user1, user2)
moderatore.following.add(user1, user2, user3, user4)
user3.richieste_in_arrivo.add(user4)

print("📝 Creazione post...")

p1 = Post.objects.create(
    autore=user1,
    caption='Tramonto sul Duomo 🌅 Una di quelle serate che non dimentichi. #milano #fotografia #tramonto',
)
p2 = Post.objects.create(
    autore=user1,
    caption='Nuovo obiettivo acquistato! Non vedo l\'ora di provarlo questo weekend. 📷',
)
p3 = Post.objects.create(
    autore=user2,
    caption='Tokyo day 3 🇯🇵 La città che non dorme mai. Assolutamente incredibile. #tokyo #travel #giappone',
)
p4 = Post.objects.create(
    autore=user2,
    caption='Pizza napoletana doc 🍕 Trovata questa piccola trattoria nascosta a Napoli. Consiglio a tutti!',
)
p5 = Post.objects.create(
    autore=user4,
    caption='Nuovo progetto illustrazione completato 🎨 Ci ho lavorato per due settimane, finalmente è pronto!',
)
p6 = Post.objects.create(
    autore=user4,
    caption='Studio in corso... le deadline non aspettano 😅 #arte #illustrazione #digitale',
)
p7 = Post.objects.create(
    autore=user1,
    caption='Questo post verrà segnalato come spam per il test del moderatore.',
)

print("❤️  Creazione like...")

p1.like.add(user2, user4, moderatore)
p2.like.add(user2)
p3.like.add(user1, user4, moderatore)
p4.like.add(user1, user4)
p5.like.add(user1, user2, moderatore)
p6.like.add(user2)

print("💬 Creazione commenti...")

c1 = Commento.objects.create(post=p1, autore=user2, testo='Che foto spettacolare! Che obiettivo hai usato? 😍')
c2 = Commento.objects.create(post=p1, autore=user4, testo='Milano è bellissima di sera ❤️')
Commento.objects.create(post=p1, autore=user1, testo='Grazie ragazzi! 50mm f/1.8', risposta_a=c1)
Commento.objects.create(post=p3, autore=user1, testo='Che fortuna! Voglio venire anche io 😭')
c3 = Commento.objects.create(post=p3, autore=user4, testo='Tokyo è nella mia bucket list da anni!')
Commento.objects.create(post=p3, autore=user2, testo='Devi assolutamente venire!', risposta_a=c3)
Commento.objects.create(post=p5, autore=user1, testo='Lavoro incredibile Sara! 🔥')
Commento.objects.create(post=p5, autore=user2, testo='Sei bravissima! Hai un profilo Behance?')

print("🚨 Creazione segnalazioni demo...")

Segnalazione.objects.create(
    segnalato_da=user2,
    post=p7,
    motivo='spam',
    descrizione='Questo post sembra contenuto spam.',
    stato='in_attesa',
)
Segnalazione.objects.create(
    segnalato_da=user4,
    post=p7,
    motivo='altro',
    descrizione='Contenuto fuori luogo.',
    stato='in_attesa',
)
Segnalazione.objects.create(
    segnalato_da=user1,
    post=p4,
    motivo='spam',
    descrizione='Test segnalazione già risolta.',
    stato='risolta',
    gestita_da=admin,  # <-- Aggiornato per usare l'admin
)

print("\n✅ Database popolato con successo!")
print("\n📋 Account demo aggiornati:")
print("   kikijiki         / admin12345      → superuser + moderatore (ADMIN)")
print("   moderatore_demo  / moderatore12345 → moderatore")
print("   mario_rossi      / user12345       → utente standard")
print("   giulia_bianchi   / user12345       → utente standard")
print("   luca_verdi       / user12345       → utente standard (account privato)")
print("   sara_neri        / user12345       → utente standard")