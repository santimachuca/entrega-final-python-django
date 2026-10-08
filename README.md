# Blog de Patrick Jane — entrega final

Aplicación web de publicaciones desarrollada con Python y Django. Permite leer posts, crear una cuenta y administrar las publicaciones propias. Las imágenes son opcionales.

## Funcionalidades

- Lista pública de publicaciones y página de detalle.
- Registro, ingreso, salida y perfil de usuario; el perfil puede editarse.
- Creación, edición y eliminación de posts desde la web.
- Solo un usuario autenticado puede crear; solo el autor puede editar o eliminar sus posts.
- Subida y visualización de imágenes opcionales, con la página adaptada a posts sin imagen.
- Panel de administración de Django en `/admin/`.

## Tecnologías

Python 3.14, Django 5.2, Pillow, SQLite, HTML y CSS. Las versiones exactas de las dependencias están en `requirements.txt`.

## Instalación y ejecución en Windows (PowerShell)

Desde la carpeta que contiene `manage.py`:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. No hace falta activar el entorno virtual si se usa directamente su ejecutable de Python, como en los comandos anteriores.

Para Linux o macOS, usar `python3 -m venv venv`, instalar con `venv/bin/python -m pip install -r requirements.txt` y ejecutar `venv/bin/python manage.py migrate` y `venv/bin/python manage.py runserver`.

La base SQLite se crea al ejecutar las migraciones. Las migraciones del proyecto se incluyen en `posts/migrations/`. Podés registrarte desde la web y crear una publicación. Si querés usar el panel de administración, creá un superusuario con `python manage.py createsuperuser` usando el intérprete del entorno virtual.

## Pruebas

```powershell
.\venv\Scripts\python.exe manage.py test
```

Las pruebas cubren las páginas públicas, registro y login, permisos de edición y eliminación, perfil y subida de imágenes.

## Configuración y archivos locales

Para desarrollo local funcionan los valores predeterminados de `blog_project/settings.py`. Antes de desplegar en un servidor, configurar las variables de entorno `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` y `DJANGO_ALLOWED_HOSTS`. El archivo `.env.example` muestra los nombres; Django lee variables de entorno del sistema, no carga `.env` automáticamente. Nunca subir claves reales.

`.gitignore` excluye los entornos virtuales, `.env`, `db.sqlite3`, los archivos compilados y las imágenes subidas en `media/`. Los archivos estáticos del sitio están en `posts/static/posts/`.

## Estructura principal

```text
blog_project/       Configuración y rutas generales
posts/              Modelo, vistas, formularios, rutas, plantillas y pruebas
posts/migrations/   Migraciones de la base de datos
manage.py           Comandos de Django
requirements.txt    Dependencias
```

## Autor

Santiago Machuca
