from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Cohort

class Command(BaseCommand):
    help = 'Limpia el acceso a cursos de estudiantes cuyas cohortes han expirado (retención finalizada).'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando limpieza de cohortes expiradas (lógica por estudiante)...')
        
        # Obtener todas las cohortes que ya finalizaron
        completed_cohorts = Cohort.objects.filter(status='completed')
        
        cohorts_archived = 0
        students_expired = 0
        
        for cohort in completed_cohorts:
            self.stdout.write(f'Procesando cohorte: {cohort.name} (ID: {cohort.id})')
            
            # Revisar cada estudiante activo en esta cohorte completada
            for student in cohort.students.all():
                if cohort.is_expired(student):
                    self.stdout.write(f'  - Estudiante {student.username} ha expirado. Removiendo acceso.')
                    cohort.students.remove(student)
                    cohort.expired_students.add(student)
                    students_expired += 1
            
            # Si la cohorte ya no tiene estudiantes activos, la archivamos
            if cohort.students.count() == 0:
                self.stdout.write(f'  - Cohorte sin estudiantes con acceso activo. Archivando cohorte.')
                cohort.status = 'archived'
                cohort.save()
                cohorts_archived += 1

        self.stdout.write(self.style.SUCCESS(f'Limpieza completada. Se removió acceso a {students_expired} estudiantes y se archivaron {cohorts_archived} cohortes.'))
