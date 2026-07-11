import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hse_canvas_project.settings')
django.setup()

from core.models import User

def seed_admin():
    email = os.environ.get('SEED_ADMIN_EMAIL', 'admin@hseacademy.com')
    password = os.environ.get('SEED_ADMIN_PASSWORD', 'admin1234')
    username = os.environ.get('SEED_ADMIN_USERNAME', 'administrador')

    if not User.objects.filter(email=email).exists():
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role='admin'
        )
        print(f"✅ Administrador creado con éxito:")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
    else:
        print(f"⚠️ El administrador con email {email} ya existe.")

if __name__ == '__main__':
    seed_admin()
