from django.utils.deprecation import MiddlewareMixin
from .models import AuditLog

class AuditMiddleware(MiddlewareMixin):
    """Middleware pour capturer les infos de requête pour l'audit"""
    
    def process_request(self, request):
        # Stocker les infos pour utilisation dans les vues
        request.audit_info = {
            'ip': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500],  # Limiter la longueur
            'path': request.path,
        }
        return None
    
    def get_client_ip(self, request):
        """Récupérer l'IP réelle du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

def log_audit(request, user, action, details=''):
    """Fonction utilitaire pour enregistrer dans l'audit"""
    if hasattr(request, 'audit_info'):
        AuditLog.objects.create(
            user=user,
            action=action,
            ip_address=request.audit_info.get('ip'),
            user_agent=request.audit_info.get('user_agent', ''),
            details=details
        )