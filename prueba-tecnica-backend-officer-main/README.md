# Preparación de la base de datos

## Arranque con Docker

Con Docker Desktop activo, ejecutar desde este directorio:

```bash
docker compose up --build
```

El contenedor descomprime `polizas_full.csv.zip`, ejecuta `setup.py` y guarda SQLite en `data/comercio_exterior.db`. La primera carga puede tardar varios minutos. En arranques posteriores reutiliza la base existente.

SQLite es un archivo y no requiere un servidor que permanezca encendido. Las dependencias del script se instalan desde `uv.lock`; `sqlite3` viene con Python.

## Autenticación

Crear `.env` con `JWT_SECRET_KEY` aleatorio y ejecutar `docker compose up --build -d`. La API queda en `http://localhost:8000/docs`.

- `POST /auth/register`: JSON `{"username":"usuario","password":"contraseña_segura"}`; devuelve `201` con id y username.
- `POST /auth/login`: formulario OAuth2 `username` y `password`; devuelve `access_token` en JSON y `Authorization: Bearer <token>` en el header de respuesta.
- `GET /auth/me`: requiere `Authorization: Bearer <token>` y devuelve el usuario autenticado.

## Dimensiones

Las rutas `GET /dimensions/paises`, `GET /dimensions/aduanas` y `GET /dimensions/tipos-regimen` requieren el token Bearer. Admiten `page` (desde 1), `page_size` (1 a 100, por defecto 20) y `q` (búsqueda por nombre). Devuelven `items`, `total`, `page` y `page_size`, ordenados por nombre.
