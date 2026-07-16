from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Cohort

class Command(BaseCommand):
    help = 'Limpia el acceso a cursos de estudiantes cuyas cohortes han expirado (retención finalizada).'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando limpieza de cohortes expiradas...')
        
        # Obtener todas las cohortes que ya finalizaron
        completed_cohorts = Cohort.objects.filter(status='completed')
        
        cohorts_processed = 0
        
        for cohort in completed_cohorts:
            if cohort.is_expired:
                self.stdout.write(f'Procesando cohorte expirada: {cohort.name} (ID: {cohort.id})')
                
                # Archivar la cohorte para que los estudiantes pierdan acceso
                cohort.status = 'archived'
                cohort.save()
                
                cohorts_processed += 1
                self.stdout.write(f'  - Cohorte marcada como archivada.')

        self.stdout.write(self.style.SUCCESS(f'Limpieza completada. Se archivaron {cohorts_processed} cohortes expiradas.'))
