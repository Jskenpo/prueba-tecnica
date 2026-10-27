# API de Analítica de Comercio Exterior

API REST para consultar pólizas de importación, administrar su creación y presentar indicadores para un dashboard. Parte del CSV y del esquema SQLite entregados con la prueba técnica.

## Decisiones técnicas

Elegí **FastAPI** porque es el framework de Python con el que más familiarizado estoy: he trabajado con él durante tres años. Esto me permite avanzar con un código que puedo mantener y explicar con claridad. Además, ofrece validación de solicitudes con Pydantic y documentación OpenAPI interactiva.

- **SQLite**: es la base proporcionada por la prueba. Vive en un archivo y no requiere un servidor de base de datos independiente.
- **`uv` y `uv.lock`**: fijan las dependencias instaladas en la imagen Docker. El proyecto utiliza Python 3.13.
- **JWT y OAuth2 Password Bearer**: el registro y el login son públicos; las demás rutas requieren un token. Las contraseñas se almacenan como hashes Argon2 y los JWT se firman con `python-jose`.
- **SQL parametrizado**: los repositorios consultan SQLite directamente. Las consultas de pólizas usan índices y paginación para limitar los resultados.
- **Caché de KPIs**: los resultados del dashboard se guardan en memoria durante un máximo de 60 segundos y se invalidan al crear una póliza. Redis todavía no está implementado.

## Estructura del repositorio

```text
app/
  routes/        # Endpoints, parámetros y dependencias de autenticación
  schemas/       # Modelos de entrada y salida de Pydantic
  controllers/   # Traducción entre HTTP y casos de uso
  services/      # Reglas de negocio, JWT y caché
  repositories/  # Consultas e inserciones SQL
  database/      # Apertura, transacción y cierre de conexiones SQLite
  main.py        # Configuración de FastAPI y registro de routers
setup.py         # ETL original: CSV a SQLite
init_db.py       # Inicialización idempotente de la base en Docker
Dockerfile
compose.yaml
pyproject.toml
uv.lock
polizas_full.csv.zip
```

El archivo `data/comercio_exterior.db` se genera al iniciar Docker y queda en el equipo anfitrión. Está excluido de Git. La tabla `users` se crea al iniciar la API; no forma parte del diagrama original de pólizas y no tiene una relación con ellas.

## Requisitos

- Docker Desktop o Docker Engine con Docker Compose.
- El archivo `polizas_full.csv.zip` en la raíz de este repositorio.
- Puerto local `8000` disponible.

## Arranque con Docker

Ejecuta los siguientes comandos **desde la carpeta que contiene `compose.yaml`**.

1. Si todavía no existe `.env`, genera una clave JWT local. El archivo está excluido de Git; conserva la misma clave entre reinicios para no invalidar los tokens vigentes:

   ```bash
   if [ ! -f .env ]; then
     printf 'JWT_SECRET_KEY=%s\n' "$(openssl rand -hex 32)" > .env
   fi
   ```

2. Construye y levanta los servicios:

   ```bash
   docker compose up --build -d
   ```

3. Consulta el estado y los logs:

   ```bash
   docker compose ps
   docker compose logs -f db-init
   docker compose logs -f api
   ```

La primera ejecución puede tardar varios minutos: `db-init` extrae el CSV del ZIP, ejecuta `setup.py` y crea `data/comercio_exterior.db`. **Es normal que `db-init` termine con código 0**; SQLite es un archivo y no necesita un contenedor ejecutándose permanentemente. En siguientes arranques se reutiliza la base si pasa la verificación de integridad y contiene ítems. `api` queda disponible en `http://localhost:8000`.

Documentación interactiva: [Swagger UI](http://localhost:8000/docs). Especificación: [OpenAPI JSON](http://localhost:8000/openapi.json).

Para detener la API sin borrar la base:

```bash
docker compose down
```

## Autenticación

| Método | Ruta | Descripción |
| --- | --- | --- |
| `POST` | `/auth/register` | Recibe JSON con `username` y `password`; devuelve `201` con el usuario, sin la contraseña. |
| `POST` | `/auth/login` | Recibe formulario OAuth2 con `username` y `password`; devuelve `access_token` y `token_type`, además del header `Authorization: Bearer <token>`. |
| `GET` | `/auth/me` | Devuelve el usuario asociado a un JWT válido. |

El token dura 30 minutos. En Swagger, el formulario de login muestra campos opcionales del estándar OAuth2 (`grant_type`, `scope`, `client_id`, `client_secret`); esta API sólo necesita `username` y `password`. Para llamar a rutas protegidas, envía `Authorization: Bearer <token>`.

Ejemplo con `curl` (usa un nombre de usuario nuevo si ya ejecutaste el registro):

```bash
curl -i -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"usuario_demo","password":"ClaveSegura123!"}'

curl -i -X POST http://localhost:8000/auth/login \
  -d 'username=usuario_demo&password=ClaveSegura123!'

# Sustituye <token> por el access_token recibido en el login.
curl -H 'Authorization: Bearer <token>' \
  http://localhost:8000/auth/me
```

## Endpoints protegidos

Todas las rutas de esta sección requieren un JWT válido.

### Dimensiones

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/dimensions/paises` | Países. |
| `GET` | `/dimensions/aduanas` | Aduanas. |
| `GET` | `/dimensions/tipos-regimen` | Tipos de régimen. |

Aceptan `page` (desde 1), `page_size` (1 a 100; por defecto 20) y `q` para buscar por nombre. Devuelven `items`, `total`, `page` y `page_size`. Ejemplo: `/dimensions/paises?q=guate&page=1&page_size=10`.

### Pólizas

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/polizas` | Lista paginada, ordenada por `id` descendente. Filtros: `correlativo`, `fecha_desde`, `fecha_hasta`, `aduana_id` y `tipo_regimen_id`. |
| `GET` | `/polizas/{id}` | Cabecera e ítems paginados. Los ítems admiten filtros `pais_id` y `sac_id`. |
| `POST` | `/polizas` | Crea la cabecera y sus ítems; devuelve `201` con el ID y el header `Location`. |

Los GET aceptan `page` y `page_size` (máximo 100). En el detalle, `items_total` indica cuántos ítems coinciden con los filtros. Las fechas se envían como `YYYY-MM-DD`.

El POST requiere `correlativo`, `fecha_declaracion`, `tipo_cambio_dolar`, `aduana_id`, `tipo_regimen_id` y entre 1 y 1000 ítems. Cada ítem requiere `sac_id`, `pais_id` y `tipo_unidad_medida_id`; los campos numéricos restantes son opcionales. **La inserción es atómica**: si falla cualquier ítem, SQLite revierte también la cabecera y los demás ítems. Un correlativo duplicado devuelve `409` y una referencia de dimensión inválida devuelve `422`.

### Dashboard

| Método | Ruta | Resultado |
| --- | --- | --- |
| `GET` | `/dashboard/kpis/totals` | Conteo de pólizas e ítems y sumas de `valor_cif_uds` y `valor_dai`. |
| `GET` | `/dashboard/kpis/top-5` | Los cinco países y cinco productos SAC con mayor suma de `valor_cif_uds`. |
| `GET` | `/dashboard/kpis/valor-por-mes?year=2025` | Valor CIF agrupado por mes de declaración; devuelve los doce meses, con cero donde no hay datos. |

Las sumas se presentan con dos decimales. La caché es **local al proceso de la API**: una escritura hecha fuera de la API puede tardar hasta 60 segundos en reflejarse. Para compartir caché entre varios procesos o contenedores habría que incorporar Redis.

## Verificación

Comprueba primero que `docker compose ps` muestre `api` en ejecución y `db-init` finalizado correctamente. En Swagger UI puedes registrar un usuario, iniciar sesión, pulsar **Authorize** con el token y ejecutar las rutas protegidas.

Para comprobar la base desde el contenedor:

```bash
docker compose exec api python -c "import sqlite3; c=sqlite3.connect('/data/comercio_exterior.db'); print(c.execute('PRAGMA integrity_check').fetchone()[0]); print(c.execute('SELECT COUNT(*) FROM polizas').fetchone()[0])"
```

Durante el desarrollo se hicieron pruebas de integración por HTTP de autenticación, dimensiones, pólizas y los tres KPIs, incluido el rollback cuando falla un ítem. **Todavía no hay una suite automatizada de tests guardada en este repositorio**; ese trabajo sigue pendiente.
