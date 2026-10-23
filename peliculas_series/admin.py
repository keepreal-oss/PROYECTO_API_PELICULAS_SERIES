from django.contrib import admin

from .models import Director, Episodio, Genero, Pelicula, Serie, Temporada

admin.site.register([Genero, Director, Pelicula, Serie, Temporada, Episodio])
admin.site.site_header = "Administración de TitanStream"
