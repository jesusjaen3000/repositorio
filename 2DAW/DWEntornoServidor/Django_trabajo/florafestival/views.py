from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Artist, Venue, Edition, Installation
from .forms import ArtistForm, VenueForm, EditionForm, InstallationForm

# Página de inicio
def index(request):
    return render(request, 'festival/index.html')


# ---------- ARTIST CRUD ----------
def artist_list(request):
    country = request.GET.get('country')
    qs = Artist.objects.all()
    if country:
        qs = qs.filter(country__iexact=country)
    return render(request, 'festival/artist_list.html', {'artists': qs})


def artist_detail(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    return render(request, 'festival/artist_detail.html', {'artist': artist})


def artist_create(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('festival:artist_list')
    else:
        form = ArtistForm()
    return render(request, 'festival/artist_form.html', {'form': form})


def artist_edit(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            form.save()
            return redirect('festival:artist_detail', pk=artist.pk)
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'festival/artist_form.html', {'form': form, 'artist': artist})


def artist_delete(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        artist.delete()
        return redirect('festival:artist_list')
    return render(request, 'festival/artist_confirm_delete.html', {'artist': artist})


# ---------- INSTALLATION ----------
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

    return render(request, 'festival/installation_list.html', {
        'installations': qs,
        'editions': editions,
        'selected_edition': selected_edition,
        'order': order
    })


def installation_detail(request, pk):
    inst = get_object_or_404(Installation, pk=pk)
    return render(request, 'festival/installation_detail.html', {'installation': inst})


def installation_create(request):
    if request.method == 'POST':
        form = InstallationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('festival:installation_list')
    else:
        form = InstallationForm()
    return render(request, 'festival/installation_form.html', {'form': form})


# ---------- VENUE ----------
def venue_list(request):
    qs = Venue.objects.all()
    return render(request, 'festival/venue_list.html', {'venues': qs})


def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    installations = venue.installations.select_related('artist', 'edition').all()
    return render(request, 'festival/venue_detail.html', {'venue': venue, 'installations': installations})


def venue_create(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('festival:venue_list')
    else:
        form = VenueForm()
    return render(request, 'festival/venue_form.html', {'form': form})


# ---------- EDITION (mínimo una acción) ----------
def edition_list(request):
    qs = Edition.objects.order_by('-year')
    return render(request, 'festival/edition_list.html', {'editions': qs})


def edition_detail(request, pk):
    edition = get_object_or_404(Edition, pk=pk)
    installations = edition.installations.select_related('artist', 'venue').all()
    return render(request, 'festival/edition_detail.html', {'edition': edition, 'installations': installations})


def edition_create(request):
    if request.method == 'POST':
        form = EditionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('festival:edition_list')
    else:
        form = EditionForm()
    return render(request, 'festival/edition_form.html', {'form': form})
