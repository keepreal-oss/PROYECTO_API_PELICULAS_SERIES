from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.db.models.deletion import ProtectedError
from . import models, forms


class NavegacionMixin:
    recurso = ''

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['recurso'] = self.recurso
        contexto['titulo'] = self.model._meta.verbose_name_plural.capitalize()
        contexto['lista_url'] = reverse('web:' + self.recurso + '_lista')
        contexto['crear_url'] = reverse('web:' + self.recurso + '_crear')
        if getattr(self, 'object', None):
            objeto = self.object
            contexto['campos'] = [(f.verbose_name, getattr(objeto, f.name)) for f in objeto._meta.fields]
            contexto['relaciones'] = [(f.verbose_name, getattr(objeto, f.name).all()) for f in objeto._meta.many_to_many]
        return contexto

    def get_success_url(self):
        return reverse('web:' + self.recurso + '_lista')


class EliminarBase(NavegacionMixin, DeleteView):
    template_name = 'crud/eliminar.html'

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            contexto = self.get_context_data(form=form)
            contexto['error'] = 'No se puede eliminar: hay películas o series asociadas. Modifica esas relaciones primero.'
            return self.render_to_response(contexto, status=409)

class PaisListView(NavegacionMixin, ListView):
    model = models.Pais
    recurso = 'pais'
    template_name = "crud/lista.html"
    ordering = "pk"


class PaisDetailView(NavegacionMixin, DetailView):
    model = models.Pais
    recurso = 'pais'
    template_name = "crud/detalle.html"


class PaisCreateView(NavegacionMixin, CreateView):
    model = models.Pais
    recurso = 'pais'
    template_name = "crud/formulario.html"
    form_class = forms.PaisForm


class PaisUpdateView(NavegacionMixin, UpdateView):
    model = models.Pais
    recurso = 'pais'
    template_name = "crud/formulario.html"
    form_class = forms.PaisForm


class PaisDeleteView(EliminarBase):
    model = models.Pais
    recurso = 'pais'
    template_name = "crud/eliminar.html"


class GeneroListView(NavegacionMixin, ListView):
    model = models.Genero
    recurso = 'genero'
    template_name = "crud/lista.html"
    ordering = "pk"


class GeneroDetailView(NavegacionMixin, DetailView):
    model = models.Genero
    recurso = 'genero'
    template_name = "crud/detalle.html"


class GeneroCreateView(NavegacionMixin, CreateView):
    model = models.Genero
    recurso = 'genero'
    template_name = "crud/formulario.html"
    form_class = forms.GeneroForm


class GeneroUpdateView(NavegacionMixin, UpdateView):
    model = models.Genero
    recurso = 'genero'
    template_name = "crud/formulario.html"
    form_class = forms.GeneroForm


class GeneroDeleteView(EliminarBase):
    model = models.Genero
    recurso = 'genero'
    template_name = "crud/eliminar.html"


class DirectorListView(NavegacionMixin, ListView):
    model = models.Director
    recurso = 'director'
    template_name = "crud/lista.html"
    ordering = "pk"


class DirectorDetailView(NavegacionMixin, DetailView):
    model = models.Director
    recurso = 'director'
    template_name = "crud/detalle.html"


class DirectorCreateView(NavegacionMixin, CreateView):
    model = models.Director
    recurso = 'director'
    template_name = "crud/formulario.html"
    form_class = forms.DirectorForm


class DirectorUpdateView(NavegacionMixin, UpdateView):
    model = models.Director
    recurso = 'director'
    template_name = "crud/formulario.html"
    form_class = forms.DirectorForm


class DirectorDeleteView(EliminarBase):
    model = models.Director
    recurso = 'director'
    template_name = "crud/eliminar.html"


class ActorListView(NavegacionMixin, ListView):
    model = models.Actor
    recurso = 'actor'
    template_name = "crud/lista.html"
    ordering = "pk"


class ActorDetailView(NavegacionMixin, DetailView):
    model = models.Actor
    recurso = 'actor'
    template_name = "crud/detalle.html"


class ActorCreateView(NavegacionMixin, CreateView):
    model = models.Actor
    recurso = 'actor'
    template_name = "crud/formulario.html"
    form_class = forms.ActorForm


class ActorUpdateView(NavegacionMixin, UpdateView):
    model = models.Actor
    recurso = 'actor'
    template_name = "crud/formulario.html"
    form_class = forms.ActorForm


class ActorDeleteView(EliminarBase):
    model = models.Actor
    recurso = 'actor'
    template_name = "crud/eliminar.html"


class PeliculaListView(NavegacionMixin, ListView):
    model = models.Pelicula
    recurso = 'pelicula'
    template_name = "crud/lista.html"
    ordering = "pk"


class PeliculaDetailView(NavegacionMixin, DetailView):
    model = models.Pelicula
    recurso = 'pelicula'
    template_name = "crud/detalle.html"


class PeliculaCreateView(NavegacionMixin, CreateView):
    model = models.Pelicula
    recurso = 'pelicula'
    template_name = "crud/formulario.html"
    form_class = forms.PeliculaForm


class PeliculaUpdateView(NavegacionMixin, UpdateView):
    model = models.Pelicula
    recurso = 'pelicula'
    template_name = "crud/formulario.html"
    form_class = forms.PeliculaForm


class PeliculaDeleteView(EliminarBase):
    model = models.Pelicula
    recurso = 'pelicula'
    template_name = "crud/eliminar.html"


class SerieListView(NavegacionMixin, ListView):
    model = models.Serie
    recurso = 'serie'
    template_name = "crud/lista.html"
    ordering = "pk"


class SerieDetailView(NavegacionMixin, DetailView):
    model = models.Serie
    recurso = 'serie'
    template_name = "crud/detalle.html"


class SerieCreateView(NavegacionMixin, CreateView):
    model = models.Serie
    recurso = 'serie'
    template_name = "crud/formulario.html"
    form_class = forms.SerieForm


class SerieUpdateView(NavegacionMixin, UpdateView):
    model = models.Serie
    recurso = 'serie'
    template_name = "crud/formulario.html"
    form_class = forms.SerieForm


class SerieDeleteView(EliminarBase):
    model = models.Serie
    recurso = 'serie'
    template_name = "crud/eliminar.html"


class TemporadaListView(NavegacionMixin, ListView):
    model = models.Temporada
    recurso = 'temporada'
    template_name = "crud/lista.html"
    ordering = "pk"


class TemporadaDetailView(NavegacionMixin, DetailView):
    model = models.Temporada
    recurso = 'temporada'
    template_name = "crud/detalle.html"


class TemporadaCreateView(NavegacionMixin, CreateView):
    model = models.Temporada
    recurso = 'temporada'
    template_name = "crud/formulario.html"
    form_class = forms.TemporadaForm


class TemporadaUpdateView(NavegacionMixin, UpdateView):
    model = models.Temporada
    recurso = 'temporada'
    template_name = "crud/formulario.html"
    form_class = forms.TemporadaForm


class TemporadaDeleteView(EliminarBase):
    model = models.Temporada
    recurso = 'temporada'
    template_name = "crud/eliminar.html"


class EpisodioListView(NavegacionMixin, ListView):
    model = models.Episodio
    recurso = 'episodio'
    template_name = "crud/lista.html"
    ordering = "pk"


class EpisodioDetailView(NavegacionMixin, DetailView):
    model = models.Episodio
    recurso = 'episodio'
    template_name = "crud/detalle.html"


class EpisodioCreateView(NavegacionMixin, CreateView):
    model = models.Episodio
    recurso = 'episodio'
    template_name = "crud/formulario.html"
    form_class = forms.EpisodioForm


class EpisodioUpdateView(NavegacionMixin, UpdateView):
    model = models.Episodio
    recurso = 'episodio'
    template_name = "crud/formulario.html"
    form_class = forms.EpisodioForm


class EpisodioDeleteView(EliminarBase):
    model = models.Episodio
    recurso = 'episodio'
    template_name = "crud/eliminar.html"


