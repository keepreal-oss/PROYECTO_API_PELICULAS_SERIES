from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from peliculas_series import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.bienvenida, name="bienvenida"),
    path("api/", include("peliculas_series.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("catalogo", RedirectView.as_view(url="/api/", permanent=False)),
    path("catalogo/", RedirectView.as_view(url="/api/", permanent=False)),
]
