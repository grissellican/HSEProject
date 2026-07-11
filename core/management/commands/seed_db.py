# core/management/commands/seed_db.py
from django.core.management.base import BaseCommand
from core.models import User
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea usuarios iniciales con diferentes roles para el LMS de HSE Academy'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        self.stdout.write("Limpiando registros antiguos de usuarios...")
        User.objects.all().delete()

        self.stdout.write("Creando usuarios de prueba...")

        # 1. Crear Administrador Principal
        admin = User.objects.create_superuser(
            username='admin@hseacademy.com', # Django requiere username único
            email='admin@hseacademy.com',
            first_name='Admin',
            lastname='HSE Academy',
            phone='+51994685185',
            role='admin',
            is_active=True
        )
        admin.set_password('admin1234')
        admin.save()
        self.stdout.write(self.style.SUCCESS('✔ Administrador creado con éxito (admin@hseacademy.com)'))

        # 2. Crear Docente de Seguridad Industrial
        teacher = User.objects.create_user(
            username='carlos.docente@hseacademy.com',
            email='carlos.docente@hseacademy.com',
            first_name='Carlos',
            lastname='Mendoza',
            phone='+51994685185',
            role='teacher',
            is_active=True
        )
        teacher.set_password('docente1234')
        teacher.save()
        self.stdout.write(self.style.SUCCESS('✔ Docente creado con éxito (carlos.docente@hseacademy.com)'))

        # 3. Crear Estudiante de Prueba
        student = User.objects.create_user(
            username='juan.estudiante@gmail.com',
            email='juan.estudiante@gmail.com',
            first_name='Juan',
            lastname='Pérez',
            phone='+51994685185',
            role='student',
            is_active=True
        )
        student.set_password('student1234')
        student.save()
        self.stdout.write(self.style.SUCCESS('✔ Estudiante creado con éxito (juan.estudiante@gmail.com)'))