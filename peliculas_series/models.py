from django.db import models
from django.core.validators import MinValueValidator

class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Director(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Actor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    titulo = models.CharField(max_length=150)
    sinopsis = models.TextField(blank=True)
    anio = models.PositiveIntegerField(validators=[MinValueValidator(1888)])
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    director = models.ForeignKey(Director, on_delete=models.PROTECT)
    generos = models.ManyToManyField(Genero)
    actores = models.ManyToManyField(Actor, blank=True)
    duracion = models.PositiveIntegerField(help_text="Duración en minutos", validators=[MinValueValidator(1)])

    def __str__(self):
        return self.titulo

class Serie(models.Model):
    titulo = models.CharField(max_length=150)
    sinopsis = models.TextField(blank=True)
    anio = models.PositiveIntegerField(validators=[MinValueValidator(1888)])
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    director = models.ForeignKey(Director, on_delete=models.PROTECT)
    generos = models.ManyToManyField(Genero)
    actores = models.ManyToManyField(Actor, blank=True)

    def __str__(self):
        return self.titulo

class Temporada(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='temporadas')
    numero = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=['serie', 'numero'], name='temporada_unica')]

    def __str__(self):
        return f'{self.serie} - Temporada {self.numero}'


class Episodio(models.Model):
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, related_name='episodios')
    numero = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    titulo = models.CharField(max_length=150)
    duracion = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=['temporada', 'numero'], name='episodio_unico')]

    def __str__(self):
        return self.titulo
