from django import forms
from .models import Artist, Venue, Edition, Installation


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'country', 'short_bio', 'website']


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'description', 'max_capacity']


class EditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = ['year', 'theme', 'start_date', 'end_date']


class InstallationForm(forms.ModelForm):
    class Meta:
        model = Installation
        fields = ['title', 'artist', 'venue', 'edition', 'opening_date', 'short_description', 'materials']