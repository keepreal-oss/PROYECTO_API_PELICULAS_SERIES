from rest_framework import serializers
from . import models

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pais
        fields = "__all__"

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genero
        fields = "__all__"

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Director
        fields = "__all__"

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Actor
        fields = "__all__"

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pelicula
        fields = "__all__"

class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Serie
        fields = "__all__"

class TemporadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Temporada
        fields = "__all__"

class EpisodioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Episodio
        fields = "__all__"

