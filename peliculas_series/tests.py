from django.test import override_settings
from rest_framework.test import APITestCase
from . import models


class CatalogoTests(APITestCase):
    def setUp(self):
        self.pais = models.Pais.objects.create(nombre='Chile')
        self.director = models.Director.objects.create(nombre='Directora')
        self.genero = models.Genero.objects.create(nombre='Drama')
        self.serie = models.Serie.objects.create(titulo='Serie base', anio=2024, pais=self.pais, director=self.director)
        self.temporada = models.Temporada.objects.create(serie=self.serie, numero=1)

    def test_crud_todos_los_recursos(self):
        contenido = dict(titulo='Ejemplo', anio=2024, pais=self.pais.pk, director=self.director.pk, generos=[self.genero.pk], actores=[])
        casos = [('paises', {'nombre': 'Argentina'}), ('generos', {'nombre': 'Comedia'}),
                 ('directores', {'nombre': 'Otro director'}), ('actores', {'nombre': 'Actriz'}),
                 ('peliculas', dict(contenido, duracion=100)), ('series', contenido),
                 ('temporadas', {'serie': self.serie.pk, 'numero': 2}),
                 ('episodios', {'temporada': self.temporada.pk, 'numero': 1, 'titulo': 'Piloto', 'duracion': 40})]
        for recurso, datos in casos:
            with self.subTest(recurso=recurso):
                url = f'/api/{recurso}/'
                response = self.client.post(url, datos, format='json')
                self.assertEqual(response.status_code, 201, response.data)
                detalle = f'{url}{response.data["id"]}/'
                self.assertEqual(self.client.get(url).status_code, 200)
                self.assertEqual(self.client.get(detalle).status_code, 200)
                self.assertEqual(self.client.put(detalle, datos, format='json').status_code, 200)
                campo = 'nombre' if 'nombre' in datos else ('titulo' if 'titulo' in datos else 'numero')
                valor = 'Actualizado' if campo != 'numero' else 3
                self.assertEqual(self.client.patch(detalle, {campo: valor}, format='json').status_code, 200)
                self.assertEqual(self.client.get(detalle).data[campo], valor)
                self.assertEqual(self.client.delete(detalle).status_code, 204)
                self.assertEqual(self.client.get(detalle).status_code, 404)

    def test_validaciones_y_relaciones(self):
        self.assertEqual(self.client.post('/api/temporadas/', {'serie': self.serie.pk, 'numero': 1}).status_code, 400)
        self.assertEqual(self.client.post('/api/episodios/', {'temporada': self.temporada.pk, 'numero': 0, 'titulo': 'Error', 'duracion': -1}).status_code, 400)
        self.assertEqual(self.client.delete(f'/api/paises/{self.pais.pk}/').status_code, 409)
        self.assertEqual(self.client.post('/api/temporadas/', {'serie': 99999, 'numero': 1}).status_code, 400)
        models.Episodio.objects.create(temporada=self.temporada, numero=1, titulo='Piloto', duracion=20)
        self.assertEqual(self.client.delete(f'/api/series/{self.serie.pk}/').status_code, 204)
        self.assertFalse(models.Temporada.objects.exists())
        self.assertFalse(models.Episodio.objects.exists())

    @override_settings(DEBUG=False)
    def test_paginas(self):
        self.assertContains(self.client.get('/'), 'TitanStream')
        self.assertEqual(self.client.get('/api/').status_code, 200)
        self.assertEqual(self.client.get('/no-existe/').status_code, 404)


class WebCrudTests(CatalogoTests):
    def test_crud_web_ocho_entidades(self):
        contenido = dict(titulo='Contenido web', anio=2024, pais=self.pais.pk, director=self.director.pk, generos=[self.genero.pk])
        casos = [('pais', models.Pais, {'nombre':'Perú'}), ('genero', models.Genero, {'nombre':'Acción'}),
                 ('director', models.Director, {'nombre':'Directora web'}), ('actor', models.Actor, {'nombre':'Actor web'}),
                 ('pelicula', models.Pelicula, dict(contenido, duracion=90)), ('serie', models.Serie, contenido),
                 ('temporada', models.Temporada, {'serie':self.serie.pk,'numero':2}),
                 ('episodio', models.Episodio, {'temporada':self.temporada.pk,'numero':1,'titulo':'Piloto','duracion':40})]
        for recurso, modelo, datos in casos:
            with self.subTest(recurso=recurso):
                lista=f'/gestion/{recurso}/'
                self.assertEqual(self.client.get(lista).status_code,200)
                self.assertEqual(self.client.get(lista+'nuevo/').status_code,200)
                antes=modelo.objects.count()
                self.assertRedirects(self.client.post(lista+'nuevo/',datos),lista)
                self.assertEqual(modelo.objects.count(),antes+1)
                obj=modelo.objects.latest('pk')
                detalle=f'{lista}{obj.pk}/'
                self.assertEqual(self.client.get(detalle).status_code,200)
                self.assertEqual(self.client.get(detalle+'editar/').status_code,200)
                campo='nombre' if 'nombre' in datos else ('titulo' if 'titulo' in datos else 'numero')
                datos=dict(datos,**{campo:4 if campo=='numero' else 'Registro editado'})
                self.assertRedirects(self.client.post(detalle+'editar/',datos),lista)
                obj.refresh_from_db()
                self.assertEqual(getattr(obj,campo),datos[campo])
                self.assertEqual(self.client.get(detalle+'eliminar/').status_code,200)
                self.assertTrue(modelo.objects.filter(pk=obj.pk).exists())
                self.assertRedirects(self.client.post(detalle+'eliminar/'),lista)
                self.assertFalse(modelo.objects.filter(pk=obj.pk).exists())

    def test_validacion_proteccion_y_csrf_web(self):
        self.assertEqual(self.client.post('/gestion/temporada/nuevo/',{'serie':self.serie.pk,'numero':1}).status_code,200)
        self.assertEqual(models.Temporada.objects.count(),1)
        self.assertEqual(self.client.post(f'/gestion/pais/{self.pais.pk}/eliminar/').status_code,409)
        self.assertTrue(models.Pais.objects.filter(pk=self.pais.pk).exists())
        from django.test import Client
        estricto=Client(enforce_csrf_checks=True)
        self.assertEqual(estricto.post('/gestion/pais/nuevo/',{'nombre':'Sin token'}).status_code,403)
