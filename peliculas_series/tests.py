from django.core.management import call_command
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Director, Episodio, Genero, Pelicula, Serie, Temporada


class CatalogoAPITests(APITestCase):
    def setUp(self):
        self.genero = Genero.objects.create(nombre="Drama")
        self.director = Director.objects.create(nombre="Directora de prueba")
        self.serie = Serie.objects.create(
            titulo="Serie base", fecha_estreno="2024-01-01",
            genero=self.genero, director=self.director,
        )
        self.temporada = Temporada.objects.create(serie=self.serie, numero=1)

    def comprobar_crud(self, nombre, modelo, datos, cambios):
        lista = reverse(f"{nombre}-list")
        response = self.client.post(lista, datos, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        pk = response.data["id"]
        detalle = reverse(f"{nombre}-detail", args=[pk])
        self.assertTrue(modelo.objects.filter(pk=pk).exists())
        listado = self.client.get(lista)
        self.assertEqual(listado.status_code, 200)
        self.assertIn(pk, [item["id"] for item in listado.data])
        self.assertEqual(self.client.get(detalle).status_code, 200)

        response = self.client.put(detalle, {**datos, **cambios}, format="json")
        self.assertEqual(response.status_code, 200, response.data)
        for campo, valor in cambios.items():
            self.assertEqual(response.data[campo], valor)
            self.assertEqual(getattr(modelo.objects.get(pk=pk), campo), valor)

        campo = next(iter(cambios))
        response = self.client.patch(detalle, {campo: datos[campo]}, format="json")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(getattr(modelo.objects.get(pk=pk), campo), datos[campo])
        self.assertEqual(self.client.delete(detalle).status_code, 204)
        self.assertFalse(modelo.objects.filter(pk=pk).exists())
        self.assertEqual(self.client.get(detalle).status_code, 404)

    def pelicula_data(self):
        return {
            "titulo": "Película de prueba", "sinopsis": "Una historia",
            "fecha_estreno": "2024-01-01", "duracion_minutos": 100,
            "genero": self.genero.pk, "director": self.director.pk,
        }

    def test_crud_genero(self):
        self.comprobar_crud("genero", Genero, {"nombre": "Comedia"}, {"nombre": "Acción"})

    def test_crud_director(self):
        self.comprobar_crud("director", Director, {"nombre": "Ana"}, {"nombre": "María"})

    def test_crud_pelicula(self):
        self.comprobar_crud("pelicula", Pelicula, self.pelicula_data(), {"titulo": "Nuevo título"})

    def test_crud_serie(self):
        self.comprobar_crud("serie", Serie, {
            "titulo": "Otra serie", "fecha_estreno": "2024-01-01",
            "genero": self.genero.pk, "director": self.director.pk,
        }, {"titulo": "Serie editada"})

    def test_crud_temporada(self):
        self.comprobar_crud("temporada", Temporada, {
            "serie": self.serie.pk, "numero": 2, "titulo": "Segunda",
        }, {"titulo": "Segunda edición"})

    def test_crud_episodio(self):
        self.comprobar_crud("episodio", Episodio, {
            "temporada": self.temporada.pk, "numero": 1,
            "titulo": "Piloto", "duracion_minutos": 40,
        }, {"titulo": "Piloto editado"})

    def test_rechaza_duracion_cero_y_negativa(self):
        for duracion in [0, -1]:
            with self.subTest(duracion=duracion):
                response = self.client.post(reverse("pelicula-list"),
                    {**self.pelicula_data(), "duracion_minutos": duracion}, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn("duracion_minutos", response.data)
        self.assertFalse(Pelicula.objects.exists())

    def test_rechaza_relacion_inexistente(self):
        response = self.client.post(reverse("pelicula-list"),
            {**self.pelicula_data(), "genero": 999999}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("genero", response.data)

    def test_put_requiere_campos_obligatorios(self):
        response = self.client.post(reverse("pelicula-list"), self.pelicula_data(), format="json")
        detalle = reverse("pelicula-detail", args=[response.data["id"]])
        self.assertEqual(self.client.put(detalle, {"titulo": "Solo título"}, format="json").status_code, 400)
        self.assertEqual(self.client.patch(detalle, {"titulo": "Solo título"}, format="json").status_code, 200)

    def test_temporada_duplicada_y_patch_duplicado(self):
        data = {"serie": self.serie.pk, "numero": 1}
        self.assertEqual(self.client.post(reverse("temporada-list"), data, format="json").status_code, 400)
        segunda = Temporada.objects.create(serie=self.serie, numero=2)
        response = self.client.patch(reverse("temporada-detail", args=[segunda.pk]), {"numero": 1}, format="json")
        self.assertEqual(response.status_code, 400)
        segunda.refresh_from_db()
        self.assertEqual(segunda.numero, 2)

    def test_episodio_duplicado(self):
        data = {"temporada": self.temporada.pk, "numero": 1, "titulo": "Piloto", "duracion_minutos": 45}
        self.assertEqual(self.client.post(reverse("episodio-list"), data, format="json").status_code, 201)
        self.assertEqual(self.client.post(reverse("episodio-list"), data, format="json").status_code, 400)

    def test_numeracion_se_puede_repetir_en_otro_padre(self):
        otra = Serie.objects.create(titulo="Otra", fecha_estreno="2024-01-01",
            genero=self.genero, director=self.director)
        response = self.client.post(reverse("temporada-list"), {"serie": otra.pk, "numero": 1}, format="json")
        self.assertEqual(response.status_code, 201)

    def test_borrado_protegido_genero_y_director(self):
        for nombre, objeto in [("genero", self.genero), ("director", self.director)]:
            with self.subTest(nombre=nombre):
                response = self.client.delete(reverse(f"{nombre}-detail", args=[objeto.pk]))
                self.assertEqual(response.status_code, 409)
                self.assertTrue(type(objeto).objects.filter(pk=objeto.pk).exists())

    def test_borrado_serie_elimina_temporadas_y_episodios(self):
        episodio = Episodio.objects.create(temporada=self.temporada, numero=1, titulo="Piloto", duracion_minutos=40)
        self.assertEqual(self.client.delete(reverse("serie-detail", args=[self.serie.pk])).status_code, 204)
        self.assertFalse(Temporada.objects.filter(pk=self.temporada.pk).exists())
        self.assertFalse(Episodio.objects.filter(pk=episodio.pk).exists())
        self.assertTrue(Genero.objects.filter(pk=self.genero.pk).exists())

    def test_campos_automaticos_no_editables(self):
        response = self.client.post(reverse("pelicula-list"),
            {**self.pelicula_data(), "created_at": "2000-01-01T00:00:00Z"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Pelicula.objects.get(pk=response.data["id"]).created_at.year, 2000)

    def test_inicio_muestra_datos_guardados_y_enlace_funcional(self):
        self.client.post(reverse("pelicula-list"), self.pelicula_data(), format="json")
        response = self.client.get("/")
        self.assertContains(response, "Película de prueba")
        self.assertContains(response, 'href="/api/"')
        self.assertEqual(self.client.get("/api/").status_code, 200)
        self.assertRedirects(self.client.get("/catalogo"), "/api/")

    @override_settings(DEBUG=False)
    def test_pagina_404(self):
        response = self.client.get("/ruta-inexistente/")
        self.assertContains(response, "Titán", status_code=404)


class DemoFixtureTests(APITestCase):
    def test_fixture_carga_seis_entidades_y_relaciones(self):
        call_command("loaddata", "demo", verbosity=0)
        for model in [Genero, Director, Pelicula, Serie, Temporada, Episodio]:
            self.assertEqual(model.objects.count(), 1)
        self.assertEqual(Episodio.objects.get().temporada.serie.titulo, "Estación del mañana")
