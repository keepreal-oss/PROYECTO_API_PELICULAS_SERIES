from django.shortcuts import render

def bienvenida(request):
    # Criterio 1: Variables y tipos de datos pertinentes
    nombre_plataforma = "TitanStream"
    total_usuarios = 1500
    
    # Estructura de datos compleja
    peliculas_destacadas = [
        {'titulo': 'Shingeki no Kyojin: The Final Chapters', 'genero': 'Anime', 'año': 2023},
        {'titulo': 'El Padrino', 'genero': 'Drama', 'año': 1972},
        {'titulo': 'Interstellar', 'genero': 'Ciencia Ficción', 'año': 2014},
    ]
    
    # Empaquetamos los datos en un diccionario para enviarlos al HTML
    contexto = {
        'nombre': nombre_plataforma,
        'usuarios': total_usuarios,
        'peliculas': peliculas_destacadas,
    }
    
    # Criterio 2.3: Integración de la lógica en la vista
    return render(request, 'bienvenida.html', contexto)

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError
from . import models, serializers

class CatalogoViewSet(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response({"detail": "Este registro está asociado a películas o series."}, status=status.HTTP_409_CONFLICT)

class PaisViewSet(CatalogoViewSet):
    queryset = models.Pais.objects.all().order_by("pk")
    serializer_class = serializers.PaisSerializer

class GeneroViewSet(CatalogoViewSet):
    queryset = models.Genero.objects.all().order_by("pk")
    serializer_class = serializers.GeneroSerializer

class DirectorViewSet(CatalogoViewSet):
    queryset = models.Director.objects.all().order_by("pk")
    serializer_class = serializers.DirectorSerializer

class ActorViewSet(CatalogoViewSet):
    queryset = models.Actor.objects.all().order_by("pk")
    serializer_class = serializers.ActorSerializer

class PeliculaViewSet(CatalogoViewSet):
    queryset = models.Pelicula.objects.all().order_by("pk")
    serializer_class = serializers.PeliculaSerializer

class SerieViewSet(CatalogoViewSet):
    queryset = models.Serie.objects.all().order_by("pk")
    serializer_class = serializers.SerieSerializer

class TemporadaViewSet(CatalogoViewSet):
    queryset = models.Temporada.objects.all().order_by("pk")
    serializer_class = serializers.TemporadaSerializer

class EpisodioViewSet(CatalogoViewSet):
    queryset = models.Episodio.objects.all().order_by("pk")
    serializer_class = serializers.EpisodioSerializer

