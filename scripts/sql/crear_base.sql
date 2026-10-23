CREATE DATABASE peliculas_series CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'peliculas_app'@'localhost' IDENTIFIED BY 'cambiar_clave';
GRANT ALL PRIVILEGES ON peliculas_series.* TO 'peliculas_app'@'localhost';
