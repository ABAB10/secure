from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """Profil utilisateur étendu"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Informations personnelles
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biographie")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Photo de profil")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    address = models.TextField(max_length=200, blank=True, verbose_name="Adresse")
    city = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    country = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    
    # Préférences
    newsletter = models.BooleanField(default=False, verbose_name="Recevoir la newsletter")
    theme = models.CharField(max_length=20, default='light', choices=[('light', 'Clair'), ('dark', 'Sombre')])
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

class AuditLog(models.Model):
    """Journal d'audit pour les 3A"""
    ACTION_CHOICES = [
        ('SIGNUP', 'Inscription'),
        ('LOGIN', 'Connexion réussie'),
        ('LOGIN_FAILED', 'Échec de connexion'),
        ('LOGOUT', 'Déconnexion'),
        ('PROFILE_UPDATE', 'Mise à jour profil'),
        ('PASSWORD_CHANGE', 'Changement mot de passe'),
        ('PROFILE_VIEW', 'Consultation profil'),
        ('ADMIN_ACCESS', 'Accès admin'),
        ('PERMISSION_DENIED', 'Tentative non autorisée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Journal d'audit"
        verbose_name_plural = "Journaux d'audit"
    
    def __str__(self):
        return f"[{self.timestamp}] {self.user or 'Anonyme'} - {self.get_action_display()}"

# Signals pour créer automatiquement le profil
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()