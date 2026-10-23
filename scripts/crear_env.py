"""Genera la configuración local sin sobrescribir un .env existente."""
from getpass import getpass
from pathlib import Path
import secrets


def main():
    destination = Path(__file__).resolve().parent.parent / ".env"
    if destination.exists():
        raise SystemExit("Ya existe .env. Revísalo manualmente; no se sobrescribió.")
    password = getpass("Contraseña del usuario titanstream_app en MySQL: ")
    if not password or "\n" in password or "\r" in password or password != password.strip():
        raise SystemExit("Usa una contraseña no vacía, sin saltos ni espacios en los extremos.")
    content = (
        f"SECRET_KEY={secrets.token_urlsafe(64)}\n"
        "DEBUG=True\nALLOWED_HOSTS=127.0.0.1,localhost\n"
        f"DB_NAME=titanstream\nDB_USER=titanstream_app\nDB_PASSWORD={password}\n"
        "DB_HOST=localhost\nDB_PORT=3306\n"
    )
    with destination.open("x", encoding="utf-8") as stream:
        stream.write(content)
    destination.chmod(0o600)
    print(".env creado. No lo subas a GitHub.")


if __name__ == "__main__":
    main()
