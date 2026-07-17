from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Cohort, Submission

class Command(BaseCommand):
    help = 'Cierra automáticamente las cohortes activas cuya fecha programada de fin ha llegado.'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando verificación de cohortes para cierre automático...')
        
        today = timezone.now().date()
        
        # Buscar cohortes activas con scheduled_end_date <= hoy
        cohorts_to_close = Cohort.objects.filter(
            status='active',
            scheduled_end_date__lte=today
        )
        
        cohorts_processed = 0
        
        for cohort in cohorts_to_close:
            self.stdout.write(f'Cerrando cohorte automáticamente: {cohort.name} (ID: {cohort.id})')
            course = cohort.course
            
            # 1. Marcar cohorte como completada
            cohort.status = 'completed'
            cohort.completed_at = today
            cohort.save()
            
            # 2. Vincular entregas existentes a esta cohorte
            cohort_students = cohort.students.all()
            Submission.objects.filter(
                assignment__module__course=course,
                student__in=cohort_students,
                cohort__isnull=True
            ).update(cohort=cohort)
            
            # 3. Remover estudiantes de la cohorte del curso activo
            for student in cohort_students:
                course.students.remove(student)
                
            # 4. Congelar contenido del curso para esta cohorte
            from core.utils import freeze_cohort_content
            freeze_cohort_content(cohort)
                
            self.stdout.write(f'  - Cohorte marcada como completada y {cohort_students.count()} estudiantes removidos del curso activo.')
            cohorts_processed += 1

        self.stdout.write(self.style.SUCCESS(f'Verificación completada. Se cerraron {cohorts_processed} cohortes automáticamente.'))
