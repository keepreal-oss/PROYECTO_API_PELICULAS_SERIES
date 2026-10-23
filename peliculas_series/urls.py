from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("paises", views.PaisViewSet)
router.register("generos", views.GeneroViewSet)
router.register("directores", views.DirectorViewSet)
router.register("actores", views.ActorViewSet)
router.register("peliculas", views.PeliculaViewSet)
router.register("series", views.SerieViewSet)
router.register("temporadas", views.TemporadaViewSet)
router.register("episodios", views.EpisodioViewSet)

urlpatterns = router.urls
