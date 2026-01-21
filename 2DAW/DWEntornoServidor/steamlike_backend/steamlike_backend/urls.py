from django.contrib import admin
from django.urls import path, include
from library.views import health, add_library_entry, library_entry_detail


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/library/entries/", add_library_entry),
    path("api/library/entries/<int:id>/", library_entry_detail),

]




