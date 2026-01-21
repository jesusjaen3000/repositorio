from django.contrib import admin
from .models import Artist, Venue, Edition, Installation


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'max_capacity')
    search_fields = ('name',)


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('year', 'theme', 'start_date', 'end_date')
    ordering = ('-year',)


@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'edition', 'opening_date', 'venue')
    list_filter = ('edition', 'artist')
    search_fields = ('title',)