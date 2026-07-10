from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.http import HttpResponseForbidden

from .models import Post, MediaPost, Commento, Segnalazione
from .forms import (
    PostForm, MediaPostForm, CommentoForm,
    SegnalazioneForm, ModeratoreSegnalazioneForm,
)
from users.models import CustomUser


# ---------------------------------------------------------------------------
# FEED
# ---------------------------------------------------------------------------

class FeedView(LoginRequiredMixin, ListView):
    """
    CBV richiesta dalle istruzioni del corso.
    Mostra i post degli utenti che l'utente corrente segue + i propri.
    """
    model               = Post
    template_name       = 'posts/feed.html'
    context_object_name = 'post_list'
    paginate_by         = 12

    def get_queryset(self):
        base = Post.objects.filter(archiviato=False, eliminato_da_moderatore=False)

        # Moderatori e superuser vedono i post generali di tutta la piattaforma,
        # non solo quelli degli utenti che seguono.
        if self.request.user.is_moderator or self.request.user.is_superuser:
            return base.prefetch_related('media', 'like', 'commenti', 'autore')

        following_ids = self.request.user.following.values_list('id', flat=True)
        return (
            base
            .filter(autore_id__in=list(following_ids) + [self.request.user.id])
            .prefetch_related('media', 'like', 'commenti', 'autore')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vista_generale'] = self.request.user.is_moderator or self.request.user.is_superuser
        return context


# ---------------------------------------------------------------------------
# CRUD POST
# ---------------------------------------------------------------------------

@login_required
def crea_post_view(request):
    post_form  = PostForm(request.POST or None)
    media_form = MediaPostForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if post_form.is_valid() and media_form.is_valid():
            caption = post_form.cleaned_data.get('caption', '')
            file    = media_form.cleaned_data.get('file')

            if not caption and not file:
                post_form.add_error('caption', "Scrivi qualcosa o aggiungi una foto/video.")
            else:
                post = post_form.save(commit=False)
                post.autore = request.user
                post.save()
                if file:
                    MediaPost.objects.create(post=post, file=file)
                messages.success(request, "Post pubblicato!")
                return redirect('posts:dettaglio', pk=post.pk)

    return render(request, 'posts/crea_post.html', {
        'post_form': post_form, 'media_form': media_form,
    })


@login_required
def dettaglio_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk, eliminato_da_moderatore=False)

    # Blocca la visualizzazione se l'autore ha account privato e l'utente non lo segue
    if (post.autore.account_privato
            and request.user not in post.autore.followers.all()
            and request.user != post.autore):
        return HttpResponseForbidden("Questo account è privato.")

    commento_form = CommentoForm()
    commenti_top  = post.commenti.filter(risposta_a__isnull=True).prefetch_related('risposte', 'like')

    return render(request, 'posts/dettaglio_post.html', {
        'post':          post,
        'commenti':      commenti_top,
        'commento_form': commento_form,
        'liked':         request.user in post.like.all(),
        'salvato':       request.user in post.salvati_da.all(),
    })


@login_required
def modifica_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.autore != request.user:
        return HttpResponseForbidden("Non puoi modificare questo post.")

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Post aggiornato.")
        return redirect('posts:dettaglio', pk=post.pk)

    return render(request, 'posts/modifica_post.html', {'form': form, 'post': post})


@login_required
def elimina_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.autore != request.user:
        return HttpResponseForbidden("Non puoi eliminare questo post.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post eliminato.")
        return redirect('posts:feed')

    return render(request, 'posts/conferma_elimina.html', {'post': post})


# ---------------------------------------------------------------------------
# LIKE / SALVA
# ---------------------------------------------------------------------------

@login_required
def toggle_like_view(request, pk):
    if request.method != 'POST':
        return HttpResponseForbidden()
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.like.all():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


@login_required
def toggle_salva_view(request, pk):
    if request.method != 'POST':
        return HttpResponseForbidden()
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.salvati_da.all():
        post.salvati_da.remove(request.user)
    else:
        post.salvati_da.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


# ---------------------------------------------------------------------------
# COMMENTI
# ---------------------------------------------------------------------------

@login_required
def aggiungi_commento_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentoForm(request.POST)
    if form.is_valid():
        commento = form.save(commit=False)
        commento.post   = post
        commento.autore = request.user
        risposta_a_id   = request.POST.get('risposta_a')
        if risposta_a_id:
            commento.risposta_a = get_object_or_404(Commento, pk=risposta_a_id)
        commento.save()
    return redirect('posts:dettaglio', pk=pk)


@login_required
def elimina_commento_view(request, pk):
    commento = get_object_or_404(Commento, pk=pk)
    post_pk  = commento.post.pk
    if commento.autore != request.user and not request.user.is_moderator:
        return HttpResponseForbidden("Non puoi eliminare questo commento.")
    if request.method == 'POST':
        commento.delete()
    return redirect('posts:dettaglio', pk=post_pk)


# ---------------------------------------------------------------------------
# SEGNALAZIONI
# ---------------------------------------------------------------------------

@login_required
def segnala_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = SegnalazioneForm(request.POST or None)
    if form.is_valid():
        seg = form.save(commit=False)
        seg.segnalato_da = request.user
        seg.post         = post
        seg.save()
        messages.success(request, "Segnalazione inviata. Grazie!")
        return redirect('posts:dettaglio', pk=pk)
    return render(request, 'posts/segnala.html', {'form': form, 'post': post})


# ---------------------------------------------------------------------------
# MODERATORE — gestione contenuti
# ---------------------------------------------------------------------------

def moderatore_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_moderator:
            return HttpResponseForbidden("Accesso riservato ai moderatori.")
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@moderatore_required
def dashboard_moderatore_view(request):
    segnalazioni = Segnalazione.objects.filter(stato='in_attesa').select_related(
        'segnalato_da', 'post', 'commento'
    )
    return render(request, 'posts/moderatore/dashboard.html', {'segnalazioni': segnalazioni})


@login_required
@moderatore_required
def gestisci_segnalazione_view(request, pk):
    segnalazione = get_object_or_404(Segnalazione, pk=pk)
    form = ModeratoreSegnalazioneForm(request.POST or None, instance=segnalazione)

    if form.is_valid():
        seg = form.save(commit=False)
        seg.gestita_da = request.user
        seg.save()
        # Se risolta → nasconde il contenuto
        if seg.stato == 'risolta' and seg.post:
            seg.post.eliminato_da_moderatore = True
            seg.post.save()
        messages.success(request, "Segnalazione aggiornata.")
        return redirect('posts:dashboard_moderatore')

    return render(request, 'posts/moderatore/gestisci_segnalazione.html', {
        'form': form, 'segnalazione': segnalazione,
    })


@login_required
@moderatore_required
def elimina_post_moderatore_view(request, pk):
    """Il moderatore può eliminare direttamente qualsiasi post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.eliminato_da_moderatore = True
        post.save()
        messages.success(request, f"Post di {post.autore.username} rimosso.")
        return redirect('posts:dashboard_moderatore')
    return render(request, 'posts/moderatore/conferma_rimozione.html', {'post': post})