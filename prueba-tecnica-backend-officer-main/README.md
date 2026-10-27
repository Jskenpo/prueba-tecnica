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

## Pólizas (lectura)

- `GET /polizas`: requiere Bearer y devuelve `items`, `total`, `page`, `page_size`. Admite `page`, `page_size` (máximo 100), `correlativo`, `fecha_desde`, `fecha_hasta` (formato `YYYY-MM-DD`), `aduana_id` y `tipo_regimen_id`. Ordena por `id` descendente.
- `GET /polizas/{id}`: devuelve la póliza y sus ítems paginados. Admite `page`, `page_size` (máximo 100), `pais_id` y `sac_id` para filtrar ítems. `items_total` cuenta los ítems que coinciden con los filtros.
- `POST /polizas`: requiere Bearer y recibe una póliza con `correlativo`, `fecha_declaracion`, `tipo_cambio_dolar`, `aduana_id`, `tipo_regimen_id` y al menos un elemento en `items`. Cada ítem requiere `sac_id`, `pais_id` y `tipo_unidad_medida_id`; los valores numéricos del ítem son opcionales. Devuelve `201` con `id`, `correlativo`, `items_created` y el header `Location`. Cabecera e ítems se guardan en una sola transacción.

## Dashboard

- `GET /dashboard/kpis/totals`: requiere Bearer y devuelve el conteo de pólizas e ítems, la suma de `valor_cif_uds` y la suma de `valor_dai`. Las sumas se redondean a dos decimales. El resultado se guarda en caché hasta 60 segundos y se invalida después de crear una póliza.
- `GET /dashboard/kpis/top-5`: requiere Bearer y devuelve `paises` y `productos_sac`, cada uno con los cinco mayores totales de `valor_cif_uds`. El resultado se guarda en caché hasta 60 segundos y se invalida después de crear una póliza.
- `GET /dashboard/kpis/valor-por-mes?year=2025`: requiere Bearer y devuelve los doce meses del año con la suma de `valor_cif_uds` según `fecha_declaracion`; los meses sin datos devuelven cero. Usa caché de hasta 60 segundos, invalidada al crear una póliza.
