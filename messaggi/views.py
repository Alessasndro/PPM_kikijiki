from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Max
from django.contrib import messages

from .models import Messaggio
from .forms import MessaggioForm
from users.models import CustomUser


@login_required
def lista_conversazioni_view(request):
    """Mostra l'elenco delle conversazioni dell'utente, con l'ultimo messaggio di ciascuna."""
    utente = request.user

    scambi = Messaggio.objects.filter(
        Q(mittente=utente) | Q(destinatario=utente)
    )

    interlocutori_ids = set()
    for m in scambi:
        interlocutori_ids.add(m.destinatario_id if m.mittente_id == utente.id else m.mittente_id)

    conversazioni = []
    for altro_id in interlocutori_ids:
        altro = CustomUser.objects.get(pk=altro_id)
        ultimo = scambi.filter(
            Q(mittente=utente, destinatario=altro) | Q(mittente=altro, destinatario=utente)
        ).order_by('-inviato_il').first()
        non_letti = scambi.filter(mittente=altro, destinatario=utente, letto=False).count()
        conversazioni.append({
            'utente': altro,
            'ultimo_messaggio': ultimo,
            'non_letti': non_letti,
        })

    conversazioni.sort(key=lambda c: c['ultimo_messaggio'].inviato_il, reverse=True)

    return render(request, 'messaggi/lista_conversazioni.html', {
        'conversazioni': conversazioni,
    })


@login_required
def conversazione_view(request, username):
    """Mostra (e permette di continuare) la conversazione con un altro utente."""
    altro = get_object_or_404(CustomUser, username=username)

    if altro == request.user:
        messages.warning(request, "Non puoi inviare messaggi a te stesso.")
        return redirect('messaggi:lista_conversazioni')

    form = MessaggioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        messaggio = form.save(commit=False)
        messaggio.mittente = request.user
        messaggio.destinatario = altro
        messaggio.save()
        return redirect('messaggi:conversazione', username=altro.username)

    thread = Messaggio.objects.filter(
        Q(mittente=request.user, destinatario=altro) | Q(mittente=altro, destinatario=request.user)
    )

    # Segna come letti i messaggi ricevuti da "altro"
    thread.filter(mittente=altro, destinatario=request.user, letto=False).update(letto=True)

    return render(request, 'messaggi/conversazione.html', {
        'altro': altro,
        'thread': thread,
        'form': form,
    })
