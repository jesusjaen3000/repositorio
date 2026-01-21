from django.contrib import admin
from django.urls import path, include

app_name = 'festival'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('festival.urls')),  # ← ESTA LÍNEA ES CLAVE
]

# Artist
path('artists/', views.artist_list, name='artist_list'),
path('artists/create/', views.artist_create, name='artist_create'),
path('artists/<int:pk>/', views.artist_detail, name='artist_detail'),
path('artists/<int:pk>/edit/', views.artist_edit, name='artist_edit'),
path('artists/<int:pk>/delete/', views.artist_delete, name='artist_delete'),


# Venue
path('venues/', views.venue_list, name='venue_list'),
path('venues/create/', views.venue_create, name='venue_create'),
path('venues/<int:pk>/', views.venue_detail, name='venue_detail'),


# Edition
path('editions/', views.edition_list, name='edition_list'),
path('editions/create/', views.edition_create, name='edition_create'),
path('editions/<int:pk>/', views.edition_detail, name='edition_detail'),


# Installation
path('installations/', views.installation_list, name='installation_list'),
path('installations/create/', views.installation_create, name='installation_create'),
path('installations/<int:pk>/', views.installation_detail, name='installation_detail'),
]