# florafestival/forms.py

from django import forms
from .models import Artist, Venue, Edition, Installation

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'country', 'short_bio', 'website']
        # Puedes añadir 'labels' o 'widgets' si quieres personalizar la apariencia

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'description', 'max_capacity']

class EditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = ['year', 'theme', 'start_date', 'end_date']
        # Usar un widget de tipo fecha (DateInput) puede mejorar la experiencia en el formulario
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class InstallationForm(forms.ModelForm):
    class Meta:
        model = Installation
        # Usamos todos los campos definidos en tu modelo Installation
        fields = ['title', 'opening_date', 'short_description', 'materials', 'artist', 'venue', 'edition']
        widgets = {
            'opening_date': forms.DateInput(attrs={'type': 'date'}),
        }