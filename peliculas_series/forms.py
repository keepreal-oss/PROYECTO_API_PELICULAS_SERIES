from django import forms
from . import models

class PaisForm(forms.ModelForm):
    class Meta:
        model = models.Pais
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'control', 'placeholder': 'Escribe el nombre'}),
        }

class GeneroForm(forms.ModelForm):
    class Meta:
        model = models.Genero
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'control', 'placeholder': 'Escribe el nombre'}),
        }

class DirectorForm(forms.ModelForm):
    class Meta:
        model = models.Director
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'control', 'placeholder': 'Escribe el nombre'}),
        }

class ActorForm(forms.ModelForm):
    class Meta:
        model = models.Actor
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'control', 'placeholder': 'Escribe el nombre'}),
        }

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = models.Pelicula
        fields = ['titulo', 'sinopsis', 'anio', 'pais', 'director', 'generos', 'actores', 'duracion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'control', 'placeholder': 'Escribe el titulo'}),
            'sinopsis': forms.Textarea(attrs={'class': 'control', 'rows': 4, 'placeholder': 'Describe el contenido'}),
            'anio': forms.NumberInput(attrs={'class': 'control', 'min': 1888}),
            'pais': forms.Select(attrs={'class': 'control'}),
            'director': forms.Select(attrs={'class': 'control'}),
            'generos': forms.SelectMultiple(attrs={'class': 'control', 'size': 5}),
            'actores': forms.SelectMultiple(attrs={'class': 'control', 'size': 5}),
            'duracion': forms.NumberInput(attrs={'class': 'control', 'min': 1}),
        }

class SerieForm(forms.ModelForm):
    class Meta:
        model = models.Serie
        fields = ['titulo', 'sinopsis', 'anio', 'pais', 'director', 'generos', 'actores']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'control', 'placeholder': 'Escribe el titulo'}),
            'sinopsis': forms.Textarea(attrs={'class': 'control', 'rows': 4, 'placeholder': 'Describe el contenido'}),
            'anio': forms.NumberInput(attrs={'class': 'control', 'min': 1888}),
            'pais': forms.Select(attrs={'class': 'control'}),
            'director': forms.Select(attrs={'class': 'control'}),
            'generos': forms.SelectMultiple(attrs={'class': 'control', 'size': 5}),
            'actores': forms.SelectMultiple(attrs={'class': 'control', 'size': 5}),
        }

class TemporadaForm(forms.ModelForm):
    class Meta:
        model = models.Temporada
        fields = ['serie', 'numero']
        widgets = {
            'serie': forms.Select(attrs={'class': 'control'}),
            'numero': forms.NumberInput(attrs={'class': 'control', 'min': 1}),
        }

class EpisodioForm(forms.ModelForm):
    class Meta:
        model = models.Episodio
        fields = ['temporada', 'numero', 'titulo', 'duracion']
        widgets = {
            'temporada': forms.Select(attrs={'class': 'control'}),
            'numero': forms.NumberInput(attrs={'class': 'control', 'min': 1}),
            'titulo': forms.TextInput(attrs={'class': 'control', 'placeholder': 'Escribe el titulo'}),
            'duracion': forms.NumberInput(attrs={'class': 'control', 'min': 1}),
        }

