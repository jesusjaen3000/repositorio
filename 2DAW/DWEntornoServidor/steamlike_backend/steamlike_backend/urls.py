from django.contrib import admin
from django.urls import path, include
from library.views import (
    health, 
    add_library_entry, 
    library_entry_detail, 
    catalog_search, 
    catalog_resolve,
    logout_view
)
from users.views import register, login_view, me_view
# Usamos solo una forma de importar para evitar confusiones


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/library/entries/", add_library_entry),
    path("api/library/entries/<int:id>/", library_entry_detail),
    path("api/register/", register),
    path("api/auth/login/", login_view),  # Nueva ruta para login
    path("api/users/me/", me_view),       # Nueva ruta para comprobación
    path("api/catalog/search/", catalog_search),
    path("api/catalog/resolve/", catalog_resolve),
    path('api/auth/logout/', logout_view, name='logout'),
    # Ruta de Depuración (Ejercicio 2)
    path('api/debug/email/test/', test_debug_email_invalido_400),

]
