from django.contrib import admin
from django.urls import path
from library.views import health, add_library_entry, library_entry_detail

# Asegúrate de importar las nuevas funciones desde sus respectivos archivos de views
from users.views import (
    register, login_view, me_view, 
    change_password, logout_view, delete_account,
    update_library_entry # Esta la hemos creado para el Ejercicio 4
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    
    # --- RUTAS DE LA BIBLIOTECA ---
    path("api/library/entries/", add_library_entry),
    # Esta ruta ahora manejará GET (detalle) y PUT (actualización completa Ejercicio 4)
    path("api/library/entries/<int:entry_id>/", update_library_entry), 
    
    # --- RUTAS DE USUARIO Y AUTENTICACIÓN ---
    path("api/register/", register),
    path("api/auth/login/", login_view),
    path("api/auth/logout/", logout_view),             # Ejercicio 6 
    
    # Gestión de perfil (me)
    # GET para ver datos, DELETE para borrar cuenta (Ejercicio 7)
    path("api/users/me/", me_view),                    
    path("api/users/me/delete/", delete_account),      # Alternativa clara para DELETE 
    
    # Ejercicio 2: Cambio de contraseña
    path("api/users/me/password/", change_password),   # Ejercicio 2 
]