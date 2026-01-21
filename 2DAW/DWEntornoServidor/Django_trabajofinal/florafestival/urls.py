# florafestival/urls.py

from django.urls import path
from . import views

app_name = 'florafestival'

urlpatterns = [
    path('', views.index, name='index'),

    # --- Artist URLs (CRUD) ---
    path('artists/', views.artist_list, name='artist_list'),
    path('artists/create/', views.artist_create, name='artist_create'),
    path('artists/<int:pk>/', views.artist_detail, name='artist_detail'),
    path('artists/<int:pk>/edit/', views.artist_edit, name='artist_edit'),
    path('artists/<int:pk>/delete/', views.artist_delete, name='artist_delete'),

    # --- Venue URLs (List, Create, Detail) ---
    path('venues/', views.venue_list, name='venue_list'),
    path('venues/create/', views.venue_create, name='venue_create'),
    path('venues/<int:pk>/', views.venue_detail, name='venue_detail'),

    # --- Edition URLs (List, Create, Detail) ---
    path('editions/', views.edition_list, name='edition_list'),
    path('editions/create/', views.edition_create, name='edition_create'),
    path('editions/<int:pk>/', views.edition_detail, name='edition_detail'),

    # --- Installation URLs (List, Create, Detail) ---
    path('installations/', views.installation_list, name='installation_list'),
    path('installations/create/', views.installation_create, name='installation_create'),
    path('installations/<int:pk>/', views.installation_detail, name='installation_detail'),
]