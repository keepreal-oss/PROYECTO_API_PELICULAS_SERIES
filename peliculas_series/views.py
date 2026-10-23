from django.db.models.deletion import ProtectedError
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Director, Episodio, Genero, Pelicula, Serie, Temporada
from .serializers import (
    DirectorSerializer, EpisodioSerializer, GeneroSerializer,
    PeliculaSerializer, SerieSerializer, TemporadaSerializer,
)


def bienvenida(request):
    contexto = {
        "nombre": "TitanStream",
        "total_peliculas": Pelicula.objects.count(),
        "total_series": Serie.objects.count(),
        "peliculas": Pelicula.objects.select_related("genero").order_by("-id")[:6],
    }
    return render(request, "bienvenida.html", contexto)


class CatalogoViewSet(viewsets.ModelViewSet):
    """CRUD compartido; convierte un borrado protegido en una respuesta clara."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "No puedes eliminar este registro: tiene películas o series asociadas."},
                status=status.HTTP_409_CONFLICT,
            )


class GeneroViewSet(CatalogoViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer


class DirectorViewSet(CatalogoViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class PeliculaViewSet(CatalogoViewSet):
    queryset = Pelicula.objects.select_related("genero", "director").all()
    serializer_class = PeliculaSerializer


class SerieViewSet(CatalogoViewSet):
    queryset = Serie.objects.select_related("genero", "director").all()
    serializer_class = SerieSerializer


class TemporadaViewSet(CatalogoViewSet):
    queryset = Temporada.objects.select_related("serie").all()
    serializer_class = TemporadaSerializer


class EpisodioViewSet(CatalogoViewSet):
    queryset = Episodio.objects.select_related("temporada__serie").all()
    serializer_class = EpisodioSerializer
