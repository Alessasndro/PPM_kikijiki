from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class RegistrazioneForm(UserCreationForm):
    """Form di registrazione pubblica — crea sempre un utente 'standard'."""
    email = forms.EmailField(required=True, help_text="Obbligatoria.")

    class Meta:
        model  = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Questa email è già registrata.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.ruolo = 'standard'   # forziamo il ruolo — non modificabile dal form pubblico
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ModificaProfiloForm(forms.ModelForm):
    """Form per modificare il proprio profilo."""
    class Meta:
        model  = CustomUser
        fields = (
            'first_name', 'last_name', 'email',
            'immagine_profilo', 'bio', 'link_sito',
            'data_nascita', 'account_privato',
        )
        widgets = {
            'first_name':      forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':       forms.TextInput(attrs={'class': 'form-control'}),
            'email':           forms.EmailInput(attrs={'class': 'form-control'}),
            'link_sito':       forms.URLInput(attrs={'class': 'form-control'}),
            'immagine_profilo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio':           forms.Textarea(attrs={'rows': 4, 'maxlength': 500, 'class': 'form-control'}),
            'data_nascita':  forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'account_privato': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Questa email è già usata da un altro account.")
        return email


class ModeratoreBanForm(forms.ModelForm):
    """Form usata SOLO dal moderatore per bannare/sbannare un utente."""
    class Meta:
        model  = CustomUser
        fields = ('is_banned',)
        labels = {'is_banned': 'Account bannato'}