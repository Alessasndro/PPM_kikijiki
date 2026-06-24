from django import forms
from .models import Post, Commento, Segnalazione


class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ('caption',)
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 4,
                'maxlength': 2200,
                'placeholder': 'Scrivi una caption…',
            }),
        }

    def clean_caption(self):
        caption = self.cleaned_data.get('caption', '').strip()
        # Una caption vuota è ammessa, ma non solo spazi bianchi
        return caption


class MediaPostForm(forms.Form):
    """Form separato per l'upload del file media (immagine/video)."""
    file = forms.FileField(
        label='Immagine o Video',
        help_text='Formati supportati: JPG, PNG, MP4. Max 50 MB.',
    )

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            ext = f.name.rsplit('.', 1)[-1].lower()
            if ext not in ('jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov'):
                raise forms.ValidationError("Formato non supportato.")
            if f.size > 50 * 1024 * 1024:
                raise forms.ValidationError("Il file supera i 50 MB.")
        return f


class CommentoForm(forms.ModelForm):
    class Meta:
        model  = Commento
        fields = ('testo',)
        widgets = {
            'testo': forms.Textarea(attrs={
                'rows': 2,
                'maxlength': 1000,
                'placeholder': 'Aggiungi un commento…',
            }),
        }

    def clean_testo(self):
        testo = self.cleaned_data.get('testo', '').strip()
        if not testo:
            raise forms.ValidationError("Il commento non può essere vuoto.")
        return testo


class SegnalazioneForm(forms.ModelForm):
    class Meta:
        model  = Segnalazione
        fields = ('motivo', 'descrizione')
        widgets = {
            'descrizione': forms.Textarea(attrs={
                'rows': 3,
                'maxlength': 500,
                'placeholder': 'Descrivi il problema (opzionale)…',
            }),
        }


class ModeratoreSegnalazioneForm(forms.ModelForm):
    """Form per il moderatore: aggiorna lo stato di una segnalazione."""
    class Meta:
        model  = Segnalazione
        fields = ('stato',)
