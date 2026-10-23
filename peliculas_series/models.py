from django.core.validators import MinValueValidator
from django.db import models


class Genero(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class Director(models.Model):
    nombre = models.CharField(max_length=120)
    nacionalidad = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=150)
    sinopsis = models.TextField(blank=True)
    fecha_estreno = models.DateField()
    duracion_minutos = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT, related_name="peliculas")
    director = models.ForeignKey(Director, on_delete=models.PROTECT, related_name="peliculas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.titulo


class Serie(models.Model):
    titulo = models.CharField(max_length=150)
    sinopsis = models.TextField(blank=True)
    fecha_estreno = models.DateField()
    finalizada = models.BooleanField(default=False)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT, related_name="series")
    director = models.ForeignKey(Director, on_delete=models.PROTECT, related_name="series")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.titulo


class Temporada(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name="temporadas")
    numero = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    titulo = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["serie", "numero"], name="temporada_unica_por_serie")
        ]

    def __str__(self):
        return f"{self.serie} - Temporada {self.numero}"


class Episodio(models.Model):
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, related_name="episodios")
    numero = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    titulo = models.CharField(max_length=150)
    sinopsis = models.TextField(blank=True)
    duracion_minutos = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["temporada", "numero"], name="episodio_unico_por_temporada")
        ]

    def __str__(self):
        return f"{self.temporada} - Episodio {self.numero}: {self.titulo}"
