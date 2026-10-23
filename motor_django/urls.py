from django.contrib import admin
from django.urls import include, path

from peliculas_series import views

urlpatterns = [
    path('api/', include('peliculas_series.urls')),
    path('admin/', admin.site.urls),
    path('', views.bienvenida, name='bienvenida'),
]
