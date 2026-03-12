from django.contrib import admin
from django.urls import path
from library.views import (
    health, 
    add_library_entry, 
    library_entry_detail, 
    catalog_search,
)
# Añadimos logout_view a la importación
from users.views import register, login_view, me_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # --- UA7 & UA8: Usuarios y Sesiones ---
    path("api/register/", register),            
    path("api/auth/login/", login_view),        
    # Ruta activada (he quitado el #)
    path("api/auth/logout/", logout_view),
    
    # Esta ruta sirve para el Ejercicio 3 (GET) y el Ejercicio 7 (DELETE)
    path("api/users/me/", me_view),
    
    # --- UA7: Biblioteca ---
    path("api/health/", health),
    path("api/library/entries/", add_library_entry),
    path("api/library/entries/<int:id>/", library_entry_detail),
    
    # --- UA9: Catálogo y Buscador ---
    path("api/catalog/search/", catalog_search), 
]