from django.contrib import admin
from django.urls import path, include
from library.views import health, add_library_entry, library_entry_detail, catalog_search, catalog_resolve 
from users.views import register, login_view, me_view, logout_view 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/library/entries/", add_library_entry),
    path("api/library/entries/<int:id>/", library_entry_detail),
    path("api/register/", register),
    path("api/auth/login/", login_view),  # ruta para login
    path("api/auth/logout/", logout_view), # Añadido: Obligatorio para cerrar sesión
    path("api/users/me/", me_view),       # ruta para comprobación
    path("api/catalog/search/", catalog_search),   # Añadido: Ejercicio 2 del PDF 4
    path("api/catalog/resolve/", catalog_resolve), # Añadido: Ejercicio 3 del PDF 4
]