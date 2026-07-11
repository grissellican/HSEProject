# HSE Academy - Plataforma LMS

HSE Academy es un Sistema de Gestión de Aprendizaje (LMS) desarrollado con **Django**. Está diseñado para gestionar de manera integral cursos de capacitación, facilitando la interacción entre administradores, profesores y estudiantes a través de una interfaz moderna y eficiente.

## 🚀 Características Clave

*   **Sistema de Roles (RBAC):** Accesos y permisos diferenciados para Administradores, Profesores y Estudiantes.
*   **Gestión de Cursos Completa:** 
    *   Administración de Sílabo (Introducción, Capacidades, Objetivos).
    *   Sistemas de Evaluación y distribución de notas configurables.
    *   Organización de contenido mediante **Módulos**.
*   **Recursos y Evaluaciones:**
    *   Soporte para Materiales Multimedia (PDFs embebidos, Videos, Enlaces).
    *   Creación de Tareas, Evaluaciones y Exámenes Online.
    *   Foros de discusión interactivos y Tablón de Avisos.
*   **Gestión de Entregas:** Calificación centralizada para profesores con estados de entregas y promedios.
*   **Sesiones en Vivo:** Integración y gestión de enlaces para clases sincrónicas (Zoom, Google Meet, etc.).
*   **Editor de Texto Enriquecido:** Integración completa de **CKEditor 5** para que el contenido subido conserve su diseño, formato e imágenes a lo largo de toda la plataforma.
*   **Interfaz Moderna:** Diseño responsivo, elegante y "premium" utilizando **Tailwind CSS**.

## 🛠️ Tecnologías Utilizadas

*   **Backend:** Python 3, Django 6
*   **Base de Datos:** MySQL (conector `mysqlclient`)
*   **Frontend:** HTML5, Tailwind CSS, FontAwesome 6
*   **Procesamiento de Archivos:** Pillow (para imágenes)
*   **Editor Rich Text:** django-ckeditor-5

---

## 💻 Instalación y Configuración Local

Sigue estos pasos para desplegar el proyecto en tu entorno local (Windows/Linux/macOS):

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd HSEProject-main
```

### 2. Crear y Activar un Entorno Virtual
Se recomienda aislar las dependencias del proyecto usando `venv`:

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**En macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
Con el entorno virtual activado, instala los paquetes necesarios:
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos (MySQL)
Este proyecto utiliza MySQL por defecto.
1. Abre tu gestor de base de datos MySQL (ej. XAMPP, MySQL Workbench o consola).
2. Crea una base de datos vacía para el proyecto.
3. Asegúrate de configurar correctamente las credenciales (usuario, contraseña, nombre de la BD y puerto) en el archivo `hse_canvas_project/settings.py` (dentro del diccionario `DATABASES`).

### 5. Aplicar Migraciones
Construye las tablas en tu base de datos local:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Cargar Datos Iniciales (Opcional pero recomendado)
Si existe un archivo `seed.py` o scripts de carga iniciales para crear usuarios de prueba, roles y cursos básicos, puedes ejecutarlo:
```bash
python seed.py
```
*(Nota: Si utilizas el sistema estándar de Django para el superusuario, puedes crear uno con `python manage.py createsuperuser`)*.

### 7. Levantar el Servidor de Desarrollo
Finalmente, inicia el proyecto:
```bash
python manage.py runserver
```
Accede a la plataforma desde tu navegador en: `http://127.0.0.1:8000/`

---

## ☁️ Implementación de Cloudflare R2 para Almacenamiento

Para almacenar los archivos y materiales subidos a la plataforma (PDFs, imágenes, etc.) en un bucket de **Cloudflare R2** en lugar de localmente, sigue estos pasos:

### 1. Instalar Librerías Requeridas
Necesitas la librería `django-storages` y `boto3` para conectar Django con la API compatible de S3:
```bash
pip install django-storages boto3
```

### 2. Actualizar las variables de entorno
Asegúrate de agregar tus credenciales de Cloudflare a tu archivo `.env` (puedes tomar como referencia `.env.example`):
```env
CLOUDFLARE_ACCOUNT_ID=tu_account_id
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_STORAGE_BUCKET_NAME=nombre-del-bucket
AWS_S3_CUSTOM_DOMAIN=tu-dominio-publico.com (Opcional)
```

### 3. Configurar Django (`settings.py`)
Agrega `storages` a tus `INSTALLED_APPS` y configura el backend de almacenamiento al final de tu archivo de settings:

```python
# Habilitar django-storages
INSTALLED_APPS += ['storages']

import os

# Configuración de S3 Boto3 para Cloudflare R2
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    CLOUDFLARE_ACCOUNT_ID = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
    AWS_S3_ENDPOINT_URL = f'https://{CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com'
    
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = None # R2 no soporta ACLs, mantener en None
    
    # URL de acceso público (Si configuraste dominio público en Cloudflare)
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')

    # Usar S3Boto3Storage como backend predeterminado para media
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## 🚀 Despliegue en Producción (VPS / Linux)

Para llevar la plataforma a un entorno de producción (ej. un VPS en DigitalOcean, AWS, Linode con Ubuntu), el estándar recomendado es usar **Gunicorn** como servidor de aplicaciones y **Nginx** como proxy inverso.

### 1. Preparar el Entorno y Variables
En tu servidor, clona el repositorio, crea tu entorno virtual y asegúrate de que tu archivo `.env` tenga la configuración estricta para producción:
```env
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,ip-del-servidor
SECRET_KEY=clave_secreta_fuerte_y_unica
```

### 2. Recolectar Archivos Estáticos
Django necesita juntar todos los archivos estáticos (CSS, JS, imágenes de diseño) en una sola carpeta para que Nginx pueda servirlos eficientemente:
```bash
python manage.py collectstatic
```

### 3. Instalar y Probar Gunicorn
Instala Gunicorn dentro de tu entorno virtual:
```bash
pip install gunicorn
```
Prueba que Gunicorn pueda levantar tu proyecto (asegúrate de permitir el puerto en tu firewall si es necesario):
```bash
gunicorn hse_canvas_project.wsgi:application --bind 0.0.0.0:8000
```

### 4. Configurar Gunicorn como Servicio (Systemd)
Para que tu aplicación se mantenga corriendo y se reinicie automáticamente si el servidor se reinicia, crea un servicio de Systemd (ej. `/etc/systemd/system/gunicorn.service`):
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=tu_usuario_linux
Group=www-data
WorkingDirectory=/ruta/a/tu/HSEProject-main
ExecStart=/ruta/a/tu/HSEProject-main/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/ruta/a/tu/HSEProject-main/hse_canvas.sock hse_canvas_project.wsgi:application

[Install]
WantedBy=multi-user.target
```
Inicia y habilita el servicio:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 5. Configurar Nginx
Crea un archivo de configuración en Nginx (ej. `/etc/nginx/sites-available/hse_canvas`):
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    # Servir archivos estáticos
    location /static/ {
        root /ruta/a/tu/HSEProject-main;
    }

    # Servir archivos multimedia (Si NO usas Cloudflare R2 / S3)
    location /media/ {
        root /ruta/a/tu/HSEProject-main;
    }

    # Pasar el tráfico a Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/ruta/a/tu/HSEProject-main/hse_canvas.sock;
    }
}
```
Habilita el sitio y reinicia Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/hse_canvas /etc/nginx/sites-enabled
sudo systemctl restart nginx
```
*(Nota: Te recomendamos encarecidamente instalar un certificado SSL gratuito utilizando **Certbot (Let's Encrypt)** para tener HTTPS en tu sitio).*

---

## 📝 Notas Adicionales para Desarrollo

*   **CKEditor 5:** Para que los archivos multimedia del editor funcionen correctamente en desarrollo, asegúrate de tener bien configuradas las rutas `MEDIA_URL` y `MEDIA_ROOT`, y que en las urls principales (urls.py) se estén sirviendo los archivos estáticos y media.
*   **Diseño UI:** Al estar usando Tailwind CSS mediante CDN en muchas plantillas, asegúrate de contar con una conexión a internet activa para visualizar correctamente los estilos al correr el proyecto de manera local.
