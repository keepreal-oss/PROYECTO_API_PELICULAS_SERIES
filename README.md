# Proyecto API de películas y series

Continuación del proyecto Django original para la evaluación 2. Se mantiene la bienvenida y su diseño. La API está en `/api/` y el administrador en `/admin/`.

## Instalación (Windows, Python 3.12 o superior)

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Editar `.env`: generar SECRET_KEY con `python -c "import secrets; print(secrets.token_urlsafe(48))"`. Cambiar la contraseña tanto en el SQL como en `.env`. No publicar `.env` ni contraseñas reales.

Con MySQL 8 instalado, abrir el cliente como administrador y ejecutar `source scripts/sql/crear_base.sql;` desde la carpeta del proyecto. El script crea base, usuario y permisos solamente para esa base. Se ejecuta una vez; si ya existen, no eliminar datos: utilizar la base existente y ajustar credenciales. Mantener `DB_ENGINE=mysql` para la entrega.

```powershell
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py createsuperuser
.venv\Scripts\python manage.py runserver
```

Abrir http://127.0.0.1:8000/api/. Para una prueba local sin MySQL, cambiar únicamente `DB_ENGINE=sqlite` en `.env`; se usará `db.sqlite3`. El entorno local preparado usa esta opción. No se verificó un servidor MySQL en esta máquina.

## Modelo

Propuesta del dominio: el README del profesor explica patrones y su código usa una biblioteca; no incluye el diseño asignado de películas y series.
| Entidad | Datos y relaciones |
|---|---|
| País, género, director, actor | Nombre único |
| Película | Título, sinopsis, año, duración en minutos, país, director, géneros y actores |
| Serie | Título, sinopsis, año, país, director, géneros y actores |
| Temporada | Serie y número, únicos en conjunto |
| Episodio | Temporada, número, título y duración; número único por temporada |

Películas y series tienen varios géneros y actores (muchos a muchos). Un país o director asociado no se puede borrar: API devuelve 409. Borrar una serie elimina sus temporadas y episodios. Los números y duraciones deben ser mayores que cero; los años comienzan en 1888. Los nombres de directores y actores se usan como identificadores únicos en esta propuesta simplificada.

## Endpoints y demostración

Todos admiten GET y POST en la colección; GET, PUT, PATCH y DELETE en `/api/recurso/id/`:

`paises`, `generos`, `directores`, `actores`, `peliculas`, `series`, `temporadas`, `episodios`.

Crear primero país, director y género con `{"nombre":"Ejemplo"}` en sus endpoints. Con sus identificadores reales, enviar a `/api/peliculas/`:

```json
{"titulo":"Mi película","sinopsis":"Ejemplo académico","anio":2024,"duracion":100,"pais":1,"director":1,"generos":[1],"actores":[]}
```

PUT reemplaza los campos editables requeridos; PATCH permite enviar solo `{"titulo":"Nuevo título"}`. DELETE devuelve 204; consultar un ID inexistente devuelve 404; datos inválidos devuelven 400. Se puede usar la interfaz navegable de DRF o Postman. La API está abierta para demostración local, sin autenticación obligatoria; no exponer esta configuración en Internet.

## Comprobaciones

```powershell
.venv\Scripts\python manage.py check
.venv\Scripts\python manage.py makemigrations --check --dry-run
.venv\Scripts\python manage.py test
```

Las pruebas cubren todos los recursos y métodos, persistencia tras PATCH, borrado, relaciones inválidas, duplicados de temporada, protección y cascadas. Para ejecutarlas en MySQL, el usuario de pruebas necesita crear la base temporal `test_peliculas_series` (permisos adicionales solo para pruebas). Para pruebas aisladas rápidas usar SQLite.

## Correspondencia con la evaluación

- Entorno: comandos de venv y dependencias fijadas.
- Django y app: `motor_django`, `peliculas_series`, settings y urls.
- Datos y registro: ocho modelos y registro completo en admin.
- Migraciones: `0001_initial.py`, aplicada y probada localmente con SQLite.
- DRF: dependencia e INSTALLED_APPS; ocho ModelSerializer y ocho ModelViewSet.
- Rutas: DefaultRouter integrado en `/api/`.
- CRUD: pruebas automáticas de GET, POST, PUT, PATCH y DELETE.
- SQL: creación de base, usuario y permisos en `scripts/sql/crear_base.sql`.
- Entorno: `.env.example` versionado y `.env` privado para ejecutar.
- GitHub: conservar historial y revisar la propuesta antes de fusionarla.


