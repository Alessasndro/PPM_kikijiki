from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseForbidden

from .models import CustomUser
from .forms import RegistrazioneForm, ModificaProfiloForm, ModeratoreBanForm


# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------

class RegistrazioneView(View):
    """CBV richiesta dalle istruzioni del corso."""
    template_name = 'users/registrazione.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('posts:feed')
        return render(request, self.template_name, {'form': RegistrazioneForm()})

    def post(self, request):
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Benvenuto, {user.username}!")
            return redirect('posts:feed')
        return render(request, self.template_name, {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            if user.is_banned:
                error = "Il tuo account è stato bannato."
            else:
                login(request, user)
                return redirect(request.GET.get('next', 'posts:feed'))
        else:
            error = "Username o password non corretti."
    return render(request, 'users/login.html', {'error': error})


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')


# ---------------------------------------------------------------------------
# PROFILO
# ---------------------------------------------------------------------------

@login_required
def profilo_view(request, username):
    """Pagina profilo pubblica di un qualsiasi utente."""
    profilo = get_object_or_404(CustomUser, username=username)
    post_list = profilo.post.filter(archiviato=False, eliminato_da_moderatore=False)

    # Se l'account è privato, mostra i post solo ai follower
    if profilo.account_privato and request.user not in profilo.followers.all() and request.user != profilo:
        post_list = profilo.post.none()

    context = {
        'profilo':        profilo,
        'post_list':      post_list,
        'is_following':   request.user in profilo.followers.all(),
        'pending_request': request.user in profilo.richieste_in_arrivo.all(),
    }
    return render(request, 'users/profilo.html', context)


@login_required
def modifica_profilo_view(request):
    if request.method == 'POST':
        form = ModificaProfiloForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilo aggiornato.")
            return redirect('users:profilo', username=request.user.username)
    else:
        form = ModificaProfiloForm(instance=request.user)
    return render(request, 'users/modifica_profilo.html', {'form': form})


# ---------------------------------------------------------------------------
# FOLLOW / UNFOLLOW
# ---------------------------------------------------------------------------

@login_required
def toggle_follow_view(request, username):
    """POST-only: segui o smetti di seguire un utente."""
    if request.method != 'POST':
        return HttpResponseForbidden()

    target = get_object_or_404(CustomUser, username=username)
    if target == request.user:
        messages.warning(request, "Non puoi seguire te stesso.")
        return redirect('users:profilo', username=username)

    if request.user in target.followers.all():
        # unfollow
        target.followers.remove(request.user)
        messages.info(request, f"Hai smesso di seguire {target.username}.")
    elif target.account_privato:
        # invia richiesta
        target.richieste_in_arrivo.add(request.user)
        messages.info(request, f"Richiesta di follow inviata a {target.username}.")
    else:
        # follow diretto
        target.followers.add(request.user)
        messages.success(request, f"Ora segui {target.username}.")

    return redirect('users:profilo', username=username)


@login_required
def gestisci_richiesta_view(request, username):
    """Accetta o rifiuta una richiesta di follow (POST)."""
    if request.method != 'POST':
        return HttpResponseForbidden()

    richiedente = get_object_or_404(CustomUser, username=username)
    azione = request.POST.get('azione')  # 'accetta' o 'rifiuta'

    if richiedente in request.user.richieste_in_arrivo.all():
        request.user.richieste_in_arrivo.remove(richiedente)
        if azione == 'accetta':
            request.user.followers.add(richiedente)
            messages.success(request, f"Hai accettato la richiesta di {richiedente.username}.")
        else:
            messages.info(request, f"Richiesta di {richiedente.username} rifiutata.")

    return redirect('users:profilo', username=request.user.username)


# ---------------------------------------------------------------------------
# MODERATORE — gestione utenti
# ---------------------------------------------------------------------------

def moderatore_required(view_func):
    """Decorator custom che verifica il ruolo moderatore."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_moderator:
            return HttpResponseForbidden("Accesso riservato ai moderatori.")
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@moderatore_required
def lista_utenti_view(request):
    utenti = CustomUser.objects.exclude(pk=request.user.pk).order_by('username')
    return render(request, 'users/moderatore/lista_utenti.html', {'utenti': utenti})


@login_required
@moderatore_required
def ban_utente_view(request, username):
    utente = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        form = ModeratoreBanForm(request.POST, instance=utente)
        if form.is_valid():
            form.save()
            stato = "bannato" if utente.is_banned else "riattivato"
            messages.success(request, f"Account {utente.username} {stato}.")
            return redirect('users:lista_utenti')
    else:
        form = ModeratoreBanForm(instance=utente)
    return render(request, 'users/moderatore/ban_utente.html', {'form': form, 'utente': utente})