"""Configuración aislada para pruebas sin MySQL ni credenciales reales."""
import os

# No son credenciales reales: DATABASES se reemplaza por SQLite en memoria abajo.
for key, value in {
    "SECRET_KEY": "solo-pruebas-no-usar-en-servidor",
    "DB_NAME": "unused", "DB_USER": "unused", "DB_PASSWORD": "unused",
}.items():
    os.environ.setdefault(key, value)

from .settings import *  # noqa: F403

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
