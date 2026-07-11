# MirrorBreaker Social (Kiki-Jiki Edition)

**Studente:** Alexandru Emilian Valentin Enache (Matricola: 7133417)
**Tipo di progetto:** Full-Stack Web Application
**Track:** Social Network
**Framework utilizzato:** Django

## Descrizione

MirrorBreaker è un Social Network completo sviluppato in Django, dotato di un'interfaccia HTML/CSS
utilizzabile direttamente dal browser, che implementa modelli, viste, form, autenticazione e permessi.
Il tema estetico è ispirato a Magic: The Gathering, con un'attenzione speciale alla figura caotica del
goblin "Kiki-Jiki", che all'interno della piattaforma riveste il ruolo di moderatore supremo.

Gli utenti possono creare un profilo, pubblicare post con foto/video, mettere like e commentare,
seguire altri utenti (anche con account privati soggetti a richiesta di follow), scambiarsi messaggi
privati e segnalare contenuti inappropriati. I moderatori gestiscono le segnalazioni, rimuovono i
contenuti e possono bannare o riattivare gli account.

## Funzionalità implementate

**Utente Standard:**
* Registrazione, login e logout.
* Creazione e gestione del proprio profilo (bio, immagine, account privato/pubblico).
* Creazione, modifica ed eliminazione dei propri post (con foto o video opzionali).
* Like e commenti (con risposte) sui post, salvataggio dei post preferiti.
* Sistema di follow/unfollow, con richieste di follow per gli account privati.
* Pagina feed con i post degli utenti seguiti + i propri.
* Messaggistica privata (conversazioni 1-a-1).
* Segnalazione di post inappropriati.
* Permessi ristretti: può modificare o eliminare unicamente i propri contenuti.

**Moderatore (es. Kiki-Jiki & Moderatore Demo):**
* Tutte le funzionalità dell'utente standard.
* Feed generale con la visione di tutti i post della piattaforma (non solo quelli degli utenti seguiti).
* Dashboard di moderazione con l'elenco delle segnalazioni in attesa.
* Gestione delle segnalazioni (risolta/ignorata) con rimozione automatica del contenuto se risolta.
* Rimozione diretta di qualsiasi post o commento.
* Elenco utenti della piattaforma e possibilità di bannare/riattivare un account.

## Istruzioni per l'installazione locale

Per eseguire correttamente il progetto in locale, segui questi passaggi in ordine:

1. Clona il repository GitHub sul tuo computer:
   ```bash
   git clone https://github.com/Alessasndro/PPM_kikijiki.git
   cd PPM_kikijiki
   ```

2. Crea e attiva un ambiente virtuale:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Su Windows: venv\Scripts\activate
   ```

3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

4. Il repository include già un database `db.sqlite3` pre-popolato: non è necessario eseguire le
   migrazioni per iniziare a esplorare il progetto. Se invece vuoi ricreare il database da zero:
   ```bash
   python manage.py migrate
   python manage.py shell < populate_db.py
   ```

5. Avvia il server di sviluppo:
   ```bash
   python manage.py runserver
   ```

6. Apri il browser su `http://127.0.0.1:8000/`.

## Database demo

Il progetto include il file `db.sqlite3` nella root del repository, già popolato con utenti, post,
commenti, messaggi e segnalazioni realistici, pronto per essere esplorato immediatamente senza dover
creare dati manualmente.

## Account demo

| Username | Password | Ruolo |
|---|---|---|
| admin_demo | admin12345 | Amministratore (superuser + moderatore) |
| moderatore_demo | moderatore12345 | Moderatore |
| kiki_jiki | moderatore12345 | Moderatore |
| mario_rossi | user12345 | Utente standard |
| giulia_bianchi | user12345 | Utente standard |
| luca_verdi | user12345 | Utente standard |
| sara_neri | user12345 | Utente standard |
| paolo_esposito | user12345 | Utente standard |
| chiara_ferro | user12345 | Utente standard |
| davide_conti | user12345 | Utente standard |
| elena_marino | user12345 | Utente standard |

## Deployment

AlexandruEnache.pythonanywhere.com

## Scenario di test consigliato

1. Accedi come `mario_rossi` (utente standard), pubblica un post e segui `giulia_bianchi`.
2.  metti like e commenta un  post.
3. Prova a modificare o eliminare un post di un altro utente: l'azione deve essere negata.
4. Invia un messaggio privato a un altro utente dalla sezione messaggi.
5. Segnala un post da un account standard.
6. Effettua il logout e accedi come `moderatore_demo`: apri la dashboard di moderazione, gestisci la
   segnalazione creata al punto 5 e verifica che il post venga nascosto.
7. Dalla lista utenti del moderatore, banna un account demo e verifica che non riesca più ad accedere.
