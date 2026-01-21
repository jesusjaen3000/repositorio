from django.db import models 


class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100, blank=True)
    short_bio = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    max_capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Edition(models.Model):
    year = models.PositiveIntegerField(unique=True)
    theme = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Edición {self.year} - {self.theme or 'sin tema'}"


class Installation(models.Model):
    title = models.CharField(max_length=250)
    opening_date = models.DateField()
    short_description = models.TextField(blank=True)
    materials = models.TextField(blank=True)

    # Relaciones – deben ir DENTRO de la clase
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='installations')
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True, related_name='installations')
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name='installations')

    class Meta:
        unique_together = ('title', 'artist', 'edition')
        ordering = ['opening_date']

    def __str__(self):
        return self.title
