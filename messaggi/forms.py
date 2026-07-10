from django import forms
from .models import Messaggio


class MessaggioForm(forms.ModelForm):
    class Meta:
        model = Messaggio
        fields = ('testo',)
        widgets = {
            'testo': forms.Textarea(attrs={
                'rows': 2,
                'maxlength': 2000,
                'placeholder': 'Scrivi un messaggio…',
                'autofocus': True,
            }),
        }

    def clean_testo(self):
        testo = self.cleaned_data.get('testo', '').strip()
        if not testo:
            raise forms.ValidationError("Il messaggio non può essere vuoto.")
        return testo
