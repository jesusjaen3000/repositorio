from django.contrib import admin
from django.urls import path
# 1. Añadimos resolve_games al import (Obligatorio para que funcione la ruta)
from library.views import (
    health, 
    add_library_entry, 
    library_entry_detail, 
    search_games, 
    resolve_games  # <--- Nuevo import obligatorio
)
from users.views import register, login_view, me_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/library/entries/", add_library_entry),
    path("api/library/entries/<int:id>/", library_entry_detail),
    
    # --- SECCIÓN CATÁLOGO (Configuración obligatoria según el PDF) ---
    # Cambiamos el prefijo a /api/catalog/ como pide el Ejercicio 2
    path("api/catalog/search/", search_games), 
    # Añadimos resolve para el flujo completo del Ejercicio 5
    path("api/catalog/resolve/", resolve_games),
    
    path("api/register/", register),
    path("api/auth/login/", login_view),
    path("api/users/me/", me_view),
]