from rest_framework import serializers

from .models import Director, Episodio, Genero, Pelicula, Serie, Temporada


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ["id", "nombre", "descripcion"]


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["id", "nombre", "nacionalidad"]


class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = ["id", "titulo", "sinopsis", "fecha_estreno", "duracion_minutos",
                  "genero", "director", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = ["id", "titulo", "sinopsis", "fecha_estreno", "finalizada",
                  "genero", "director", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class TemporadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporada
        fields = ["id", "serie", "numero", "titulo"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Temporada.objects.all(), fields=["serie", "numero"],
                message="Esta serie ya tiene una temporada con ese número.",
            )
        ]


class EpisodioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episodio
        fields = ["id", "temporada", "numero", "titulo", "sinopsis", "duracion_minutos"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Episodio.objects.all(), fields=["temporada", "numero"],
                message="Esta temporada ya tiene un episodio con ese número.",
            )
        ]
