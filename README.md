# TitanStream · API de películas y series

Proyecto Django del repositorio `keepreal-oss/PROYECTO_API_PELICULAS_SERIES`, ampliado para la Evaluación 2 de Backend. Conserva la página TitanStream y agrega persistencia y una API REST con CRUD para seis entidades.

**Empieza por [GUIA_EVALUACION_2.md](GUIA_EVALUACION_2.md)**: explica la instalación en Windows, el código, las relaciones, las pruebas y la defensa oral. El alcance elegido es un catálogo: un género principal y un director principal por película/serie; una serie tiene temporadas y una temporada tiene episodios. No reproduce archivos de video.

## Entorno

- Python 3.12 recomendado; código verificado con Python 3.12.14.
- Django 5.2.18, Django REST Framework 3.16.1, python-decouple 3.8.
- MySQL 8.0.11 o superior, con el servicio iniciado, y mysqlclient 2.2.8.
- Se eligió Django 5.2 para trabajar con el entorno verificado; no reutilices el entorno virtual anterior sin instalar estas dependencias.

## Inicio en Windows PowerShell

Ejecuta desde la carpeta que contiene `manage.py`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

1. Abre `sql/01_crear_base_datos.sql` en MySQL Workbench. En una copia local, reemplaza `CAMBIAR_CLAVE_LOCAL` por tu contraseña y ejecuta el SQL como administrador. No publiques esa copia con la clave real.
2. Ejecuta el siguiente bloque. La primera línea solicita la misma contraseña y genera `.env` con una nueva `SECRET_KEY`, sin sobrescribir un archivo existente:

```powershell
.\.venv\Scripts\python.exe scripts/crear_env.py
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

La creación de `.env` se hace **una sola vez**.

URLs locales:

- Inicio: http://127.0.0.1:8000/
- API navegable: http://127.0.0.1:8000/api/
- Administración: http://127.0.0.1:8000/admin/

Opcional, **solo sobre un catálogo recién creado y vacío**:

```powershell
.\.venv\Scripts\python.exe manage.py loaddata demo
```

La fixture usa identificadores fijos y podría sobrescribir registros con esos IDs. Los títulos y personas de demostración son ficticios.

## Endpoints

| Entidad | Colección: GET y POST | Detalle: GET, PUT, PATCH y DELETE |
|---|---|---|
| Género | `/api/generos/` | `/api/generos/{id}/` |
| Director | `/api/directores/` | `/api/directores/{id}/` |
| Película | `/api/peliculas/` | `/api/peliculas/{id}/` |
| Serie | `/api/series/` | `/api/series/{id}/` |
| Temporada | `/api/temporadas/` | `/api/temporadas/{id}/` |
| Episodio | `/api/episodios/` | `/api/episodios/{id}/` |

La API es una práctica local con `AllowAny`. No desplegarla públicamente con escritura anónima. Los campos relacionados reciben IDs existentes.

## Pruebas

Pruebas aisladas, sin credenciales ni servidor MySQL:

```powershell
.\.venv\Scripts\python.exe manage.py test --settings=motor_django.test_settings -v 2
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run --settings=motor_django.test_settings
```

Si solo deseas ejecutar los tests en un equipo sin las bibliotecas del cliente MySQL, puedes instalar `requirements-test.txt` en otro entorno. Esto **no prepara el servidor de la entrega**.

Para probar con MySQL, ejecuta primero `sql/02_permisos_pruebas.sql` como administrador y luego:

```powershell
.\.venv\Scripts\python.exe manage.py test -v 2
```

Django crea y elimina una base aparte llamada `test_titanstream`. No apuntes esa base de pruebas a datos que quieras conservar.

Resultado verificado durante esta preparación: **18 pruebas correctas en SQLite**, `check` sin problemas y `makemigrations --check` sin cambios pendientes. No se verificó la ejecución en MySQL en este entorno.

## Archivos importantes

| Archivo | Función |
|---|---|
| `peliculas_series/models.py` | Seis tablas y sus relaciones |
| `peliculas_series/migrations/0001_initial.py` | Historial inicial del esquema |
| `peliculas_series/serializers.py` | Campos de entrada/salida y validación |
| `peliculas_series/views.py` | Página inicial y ModelViewSets |
| `peliculas_series/urls.py` | Router de los seis recursos |
| `motor_django/urls.py` | Integra la API en `/api/` |
| `motor_django/settings.py` | DRF, MySQL y variables de entorno |
| `peliculas_series/admin.py` | Registra los seis modelos |
| `peliculas_series/tests.py` | CRUD y casos inválidos |
| `sql/` | Base, usuario y permisos |
| `.env.example` | Nombres de variables, sin claves reales |
| `scripts/crear_env.py` | Crea `.env` local con clave aleatoria |
| `docs/api_ejemplos.http` | Peticiones de práctica |

La clave que estaba en el `settings.py` original deja de utilizarse. `crear_env.py` genera una nueva; el historial antiguo de Git no se reescribe.
