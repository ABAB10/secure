from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentification
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard & Profil
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('password/change/', views.password_change_view, name='password_change'),
    
    # Gestion de compte
    path('delete/', views.delete_account_view, name='delete_account'),
    
    # Audit (admin seulement)
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),
]