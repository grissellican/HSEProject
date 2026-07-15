from .models import PlatformSetting

def platform_settings(request):
    """
    Inyecta la configuración global de la plataforma (como el logo y nombre) 
    en todas las plantillas.
    """
    settings = PlatformSetting.get_settings()
    return {
        'platform_settings': settings
    }
