from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import Profile

class SignUpForm(UserCreationForm):
    """Formulaire d'inscription avec validation renforcée"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemple@email.com'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Jean'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dupont'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '06 12 34 56 78'
        })
    )
    
    newsletter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'newsletter')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personnalisation du champ username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
        self.fields['username'].help_text = "Requis. 150 caractères maximum. Lettres, chiffres et @/./+/-/_"
        
        # Personnalisation du champ mot de passe
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        
        # Message d'aide personnalisé pour le mot de passe (règles de sécurité)
        self.fields['password1'].help_text = """
        <ul class="text-muted small mt-1" style="padding-left: 1rem; margin-bottom: 0;">
            <li>Au moins 8 caractères</li>
            <li>Au moins une majuscule (A-Z)</li>
            <li>Au moins un chiffre (0-9)</li>
            <li>Au moins un caractère spécial (!@#$%^&*())</li>
            <li>Ne pas ressembler à vos informations personnelles</li>
        </ul>
        """
        
        # Personnalisation du champ confirmation mot de passe
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })
        self.fields['password2'].help_text = "Entrez le même mot de passe que précédemment."
    
    def clean_email(self):
        """Vérifie que l'email n'est pas déjà utilisé"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre compte.")
        return email
    
    def clean_username(self):
        """Vérifie que le nom d'utilisateur n'est pas déjà utilisé"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username
    
    def save(self, commit=True):
        """Sauvegarde l'utilisateur et son profil"""
        user = super().save(commit=False)
        
        if commit:
            user.save()
            # Mettre à jour ou créer le profil
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone', '')
            profile.newsletter = self.cleaned_data.get('newsletter', False)
            profile.save()
        
        return user


class LoginForm(AuthenticationForm):
    """Formulaire de connexion personnalisé"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })


class UserUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour des informations utilisateur"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_username(self):
        """Vérifie que le nouveau nom d'utilisateur n'est pas déjà pris"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username


class ProfileUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour du profil utilisateur"""
    
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'phone', 'birth_date', 'address', 'city', 'country', 'newsletter', 'theme']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Parlez-nous un peu de vous...'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '06 12 34 56 78'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Numéro et rue'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pays'
            }),
            'newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'theme': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('light', 'Clair'),
                ('dark', 'Sombre')
            ]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le champ birth_date optionnel
        self.fields['birth_date'].required = False
        self.fields['bio'].required = False
        self.fields['address'].required = False
        self.fields['city'].required = False
        self.fields['country'].required = False


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulaire de changement de mot de passe avec les mêmes règles"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ancien mot de passe'
        })
        
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe'
        })
        
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le nouveau mot de passe'
        })
        
        # Message d'aide personnalisé pour le nouveau mot de passe
        self.fields['new_password1'].help_text = """
        <ul class="text-muted small mt-1" style="padding-left: 1rem;">
            <li>Au moins 8 caractères</li>
            <li>Au moins une majuscule (A-Z)</li>
            <li>Au moins un chiffre (0-9)</li>
            <li>Au moins un caractère spécial (!@#$%^&*())</li>
        </ul>
        """