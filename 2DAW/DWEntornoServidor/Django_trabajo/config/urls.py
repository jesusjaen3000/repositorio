from django.urls import path, include
urlpatterns = [
    path('', include('festival.urls', namespace='festival')),
    path('admin/', admin.site.urls),
]
from . import views


app_name = 'festival'


urlpatterns = [
path('', views.index, name='index'),


# Artist
path('artists/', views.artist_list, name='artist_list'),
path('artists/create/', views.artist_create, name='artist_create'),
path('artists/<int:pk>/', views.artist_detail, name='artist_detail'),
path('artists/<int:pk>/edit/', views.artist_edit, name='artist_edit'),
path('artists/<int:pk>/delete/', views.artist_delete, name='artist_delete'),


# Installation
path('installations/', views.installation_list, name='installation_list'),
path('installations/create/', views.installation_create, name='installation_create'),
path('installations/<int:pk>/', views.installation_detail, name='installation_detail'),
]