from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count # Importación necesaria para la consulta en index

from .models import Artist, Venue, Edition, Installation
from .forms import ArtistForm, VenueForm, EditionForm, InstallationForm


# -----------------------------------------------------
# FUNCIÓN DE PÁGINA DE INICIO (INDEX)
# -----------------------------------------------------
def index(request):
    """Página de inicio con enlaces de navegación y datos dinámicos."""
    try:
        # Consulta dinámica: artistas con más instalaciones (puede fallar si la BD está vacía o mal migrada)
        top_artists = Artist.objects.annotate(num_works=Count('installations')).order_by('-num_works')[:5]
    except Exception:
        # En caso de error (ej: la tabla no existe o es la primera ejecución), se usa una lista vacía
        top_artists = [] 

    context = {'top_artists': top_artists}
    # CORREGIDO: Usar 'florafestival/index.html'
    return render(request, 'florafestival/index.html', context)


# -----------------------------------------------------
# ARTIST CRUD (Artistas)
# -----------------------------------------------------
def artist_list(request):
    country = request.GET.get('country')
    qs = Artist.objects.all()
    if country:
        qs = qs.filter(country__iexact=country)
    
    countries = Artist.objects.values_list('country', flat=True).distinct() # Para el filtro

    # CORREGIDO: Usar 'florafestival/artist_list.html'
    return render(request, 'florafestival/artist_list.html', {'artists': qs, 'countries': countries})


def artist_detail(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    # CORREGIDO: Usar 'florafestival/artist_detail.html'
    return render(request, 'florafestival/artist_detail.html', {'artist': artist})


def artist_create(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            # CORREGIDO: Usar 'florafestival:artist_list'
            return redirect('florafestival:artist_list') 
    else:
        form = ArtistForm()
    # CORREGIDO: Usar 'florafestival/artist_form.html'
    return render(request, 'florafestival/artist_form.html', {'form': form, 'form_title': 'Crear Artista'})


def artist_edit(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            form.save()
            # CORREGIDO: Usar 'florafestival:artist_detail'
            return redirect('florafestival:artist_detail', pk=artist.pk)
    else:
        form = ArtistForm(instance=artist)
    # CORREGIDO: Usar 'florafestival/artist_form.html'
    return render(request, 'florafestival/artist_form.html', {'form': form, 'artist': artist, 'form_title': f'Editar {artist.name}'})


def artist_delete(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        artist.delete()
        # CORREGIDO: Usar 'florafestival:artist_list'
        return redirect('florafestival:artist_list')
    # CORREGIDO: Usar 'florafestival/artist_confirm_delete.html'
    return render(request, 'florafestival/artist_confirm_delete.html', {'artist': artist})


# -----------------------------------------------------
# INSTALLATION (Instalaciones)
# -----------------------------------------------------
def installation_list(request):
    # filtros y orden
    edition_id = request.GET.get('edition')
    order = request.GET.get('order', 'asc')
    qs = Installation.objects.select_related('artist', 'venue', 'edition').all()

    if edition_id:
        qs = qs.filter(edition__id=edition_id)

    if order == 'desc':
        qs = qs.order_by('-opening_date')
    else:
        qs = qs.order_by('opening_date')

    # opcional: devolver JSON si se pide ?format=json
    if request.GET.get('format') == 'json':
        data = []
        for inst in qs:
            data.append({
                'id': inst.id,
                'title': inst.title,
                'opening_date': inst.opening_date.isoformat(),
                'artist': inst.artist.name,
                'venue': inst.venue.name if inst.venue else None,
                'edition': inst.edition.year,
            })
        return JsonResponse({'installations': data})

    editions = Edition.objects.order_by('-year')
    selected_edition = None
    if edition_id:
        try:
            selected_edition = Edition.objects.get(pk=edition_id)
        except Edition.DoesNotExist:
            selected_edition = None

    # CORREGIDO: Usar 'florafestival/installation_list.html'
    return render(request, 'florafestival/installation_list.html', {
        'installations': qs,
        'editions': editions,
        'selected_edition': selected_edition,
        'order': order
    })


def installation_detail(request, pk):
    inst = get_object_or_404(Installation, pk=pk)
    # CORREGIDO: Usar 'florafestival/installation_detail.html'
    return render(request, 'florafestival/installation_detail.html', {'installation': inst})


def installation_create(request):
    if request.method == 'POST':
        form = InstallationForm(request.POST)
        if form.is_valid():
            form.save()
            # CORREGIDO: Usar 'florafestival:installation_list'
            return redirect('florafestival:installation_list')
    else:
        form = InstallationForm()
    # CORREGIDO: Usar 'florafestival/installation_form.html'
    return render(request, 'florafestival/installation_form.html', {'form': form, 'form_title': 'Crear Instalación'})


# -----------------------------------------------------
# VENUE (Localizaciones)
# -----------------------------------------------------
def venue_list(request):
    qs = Venue.objects.all()
    # CORREGIDO: Usar 'florafestival/venue_list.html'
    return render(request, 'florafestival/venue_list.html', {'venues': qs})


def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    # Usar .all() al final
    installations = venue.installations.select_related('artist', 'edition').all()
    # CORREGIDO: Usar 'florafestival/venue_detail.html'
    return render(request, 'florafestival/venue_detail.html', {'venue': venue, 'installations': installations})


def venue_create(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            # CORREGIDO: Usar 'florafestival:venue_list'
            return redirect('florafestival:venue_list')
    else:
        form = VenueForm()
    # CORREGIDO: Usar 'florafestival/venue_form.html'
    return render(request, 'florafestival/venue_form.html', {'form': form, 'form_title': 'Crear Localización'})


# -----------------------------------------------------
# EDITION (Ediciones)
# -----------------------------------------------------
def edition_list(request):
    qs = Edition.objects.order_by('-year')
    # CORREGIDO: Usar 'florafestival/edition_list.html'
    return render(request, 'florafestival/edition_list.html', {'editions': qs})


def edition_detail(request, pk):
    edition = get_object_or_404(Edition, pk=pk)
    installations = edition.installations.select_related('artist', 'venue').all()
    # CORREGIDO: Usar 'florafestival/edition_detail.html'
    return render(request, 'florafestival/edition_detail.html', {'edition': edition, 'installations': installations})


def edition_create(request):
    if request.method == 'POST':
        form = EditionForm(request.POST)
        if form.is_valid():
            form.save()
            # CORREGIDO: Usar 'florafestival:edition_list'
            return redirect('florafestival:edition_list')
    else:
        form = EditionForm()
    # CORREGIDO: Usar 'florafestival/edition_form.html'
    return render(request, 'florafestival/edition_form.html', {'form': form, 'form_title': 'Crear Edición'})