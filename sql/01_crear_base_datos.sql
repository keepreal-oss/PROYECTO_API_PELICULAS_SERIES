-- Ejecutar con una cuenta administradora de MySQL.
-- Cambiar CAMBIAR_CLAVE_LOCAL antes de ejecutar; usar la misma clave en .env.
-- Si base/usuario ya existen, revisar su configuración: no borrar datos para repetir.
CREATE DATABASE titanstream CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'titanstream_app'@'localhost' IDENTIFIED BY 'CAMBIAR_CLAVE_LOCAL';
GRANT ALL PRIVILEGES ON titanstream.* TO 'titanstream_app'@'localhost';
-- CREATE USER y GRANT aplican los permisos sin requerir FLUSH PRIVILEGES.
