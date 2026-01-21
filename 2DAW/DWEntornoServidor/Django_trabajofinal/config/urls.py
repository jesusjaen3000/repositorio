# config/urls.py

from django.contrib import admin
from django.urls import path, include # <--- ¡IMPORTANTE: Usar 'include' aquí!

urlpatterns = [
    # Ruta para el panel de administración
    path('admin/', admin.site.urls),
    
    # Incluye todas las URLs de la aplicación 'florafestival'
    # path('', ...) hace que las URLs de 'florafestival' comiencen desde la raíz del sitio.
    path('', include('florafestival.urls')), 
]