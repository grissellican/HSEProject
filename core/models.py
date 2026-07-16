from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('teacher', 'Docente'),
        ('student', 'Estudiante'),
    )
    lastname = models.CharField(max_length=150, blank=True, verbose_name="Apellidos")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    show_phone = models.BooleanField(default=True, verbose_name="Mostrar teléfono a estudiantes")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Rol")
    profile_picture = models.ImageField(upload_to='profiles/pictures/', blank=True, null=True, verbose_name="Foto de Perfil")
    presentation = models.TextField(blank=True, verbose_name="Presentación Docente")

    def __str__(self):
        return f"{self.first_name} {self.lastname} ({self.get_role_display()})"


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre del Curso")
    category = models.CharField(max_length=150, default="Ingeniería de Seguridad", verbose_name="Especialidad")
    welcome_description = models.TextField(blank=True, verbose_name="Mensaje de Bienvenida")
    start_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    cover_image = models.ImageField(upload_to='courses/covers/', blank=True, null=True, verbose_name="Imagen de Portada (Archivo)")
    image_url = models.URLField(blank=True, verbose_name="Imagen de Portada (URL)")
    
    # CAPACIDADES
    capacities = models.TextField(blank=True, verbose_name="Capacidades")
    
    # SÍLABO
    syllabus_introduction = models.TextField(blank=True, verbose_name="Sílabo: Introducción")
    syllabus_objectives = models.TextField(blank=True, verbose_name="Sílabo: Objetivos")
    syllabus_modules_outline = models.TextField(blank=True, verbose_name="Sílabo: Unidades/Módulos")
    
    # SISTEMA DE EVALUACIÓN
    evaluation_system_description = models.TextField(blank=True, verbose_name="Sistema de Evaluación: Redacción")
    
    # PERMISOS
    allow_teacher_edit_syllabus = models.BooleanField(default=True, verbose_name="Permitir al docente editar Sílabo y Evaluación")
    
    # RELACIONES COMPLEMENTARIAS REQUERIDAS POR EL CANVAS
    teacher = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="courses_taught", 
        verbose_name="Docente Asignado"
    )
    students = models.ManyToManyField(
        User, 
        related_name="enrolled_courses", 
        blank=True, 
        verbose_name="Estudiantes Matriculados"
    )

    def get_cover_image(self):
        """Devuelve la URL de portada, priorizando el archivo subido sobre la URL."""
        if self.cover_image:
            return self.cover_image.url
        if self.image_url:
            return self.image_url
        return None

    def __str__(self):
        return self.title


class EvaluationImage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="evaluation_images", verbose_name="Curso")
    title = models.CharField(max_length=200, verbose_name="Título de la Imagen")
    image = models.ImageField(upload_to='courses/evaluations/', verbose_name="Imagen")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class SyllabusUnit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="syllabus_units", verbose_name="Curso")
    title = models.CharField(max_length=255, verbose_name="Título de la Unidad")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.order}. {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments", verbose_name="Estudiante")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments", verbose_name="Curso")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inscripción")

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.first_name} inscrito en {self.course.title}"


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name="Curso")
    title = models.CharField(max_length=200, verbose_name="Título del Módulo")
    description = models.TextField(blank=True, verbose_name="Descripción")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_visible = models.BooleanField(default=True, verbose_name="Visible para estudiantes")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.order}. {self.title}"


class Material(models.Model):
    MATERIAL_TYPES = (
        ('pdf', 'Documento PDF'),
        ('video', 'Video'),
        ('document', 'Documento'),
        ('other', 'Otro'),
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='materials', verbose_name="Módulo")
    title = models.CharField(max_length=200, verbose_name="Título del Material")
    description = models.TextField(blank=True, verbose_name="Descripción")
    file = models.FileField(upload_to='materials/%Y/%m/', verbose_name="Archivo")
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES, default='document', verbose_name="Tipo")
    is_visible = models.BooleanField(default=True, verbose_name="Visible para estudiantes")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Subida")

    class Meta:
        ordering = ['uploaded_at']

    def save(self, *args, **kwargs):
        if self.file and self.file.name:
            import os
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext == '.pdf':
                self.material_type = 'pdf'
            elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.mkv']:
                self.material_type = 'video'
            else:
                self.material_type = 'document'
        super().save(*args, **kwargs)

    @property
    def file_basename(self):
        import os
        if self.file and self.file.name:
            return os.path.basename(self.file.name)
        return ''

    @property
    def is_office_document(self):
        import os
        if self.file and self.file.name:
            ext = os.path.splitext(self.file.name)[1].lower()
            return ext in ['.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx']
        return False

    def __str__(self):
        return self.title


class Assignment(models.Model):
    ASSIGNMENT_TYPES = (
        ('tarea', 'Tarea'),
        ('evaluacion', 'Evaluación'),
        ('examen_online', 'Examen Online (Plataforma)'),
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assignments', verbose_name="Módulo")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Instrucciones")
    delivery_specifications = models.TextField(blank=True, verbose_name="Especificaciones de Entrega")
    evaluation_criteria = models.TextField(blank=True, verbose_name="Criterios de Evaluación")
    attached_file = models.FileField(upload_to='assignments/docs/', blank=True, null=True, verbose_name="Documento Guía")
    assignment_type = models.CharField(max_length=30, choices=ASSIGNMENT_TYPES, default='tarea', verbose_name="Tipo")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha Límite de Entrega")
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=20, verbose_name="Puntaje Máximo")
    max_attempts = models.PositiveIntegerField(default=1, verbose_name="Número de intentos permitidos", help_text="Déjalo en 0 para intentos ilimitados.")
    is_visible = models.BooleanField(default=True, verbose_name="Visible para estudiantes")
    allow_backtracking = models.BooleanField(default=False, verbose_name="Permitir retroceder a preguntas anteriores (Exámenes)")
    show_all_questions = models.BooleanField(default=False, verbose_name="Mostrar todas las preguntas en una sola página (Exámenes)", help_text="Si no marcas esta casilla, las preguntas se mostrarán una por una al estudiante.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.get_assignment_type_display()}: {self.title}"

    @property
    def filename(self):
        if self.attached_file:
            import os
            return os.path.basename(self.attached_file.name)
        return ""


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions', verbose_name="Tarea/Evaluación")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions', verbose_name="Estudiante")
    file = models.FileField(upload_to='submissions/%Y/%m/', blank=True, null=True, verbose_name="Archivo Entregado")
    text_content = models.TextField(blank=True, verbose_name="Respuesta de Texto")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Entrega")
    attempts = models.PositiveIntegerField(default=1, verbose_name="Intentos realizados")
    # Calificación
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Calificación")
    feedback = models.TextField(blank=True, verbose_name="Retroalimentación del Docente")
    graded_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Calificación")

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    @property
    def is_graded(self):
        return self.score is not None

    @property
    def percentage(self):
        if self.score is not None and self.assignment.max_score > 0:
            return round((self.score / self.assignment.max_score) * 100, 1)
        return None

    def __str__(self):
        return f"{self.student.first_name} - {self.assignment.title}"


class SubmissionFile(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='files', verbose_name="Entrega")
    file = models.FileField(upload_to='submissions/%Y/%m/', verbose_name="Archivo")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Archivo de {self.submission.student.first_name} para {self.submission.assignment.title}"

    @property
    def is_office_document(self):
        import os
        if self.file and self.file.name:
            ext = os.path.splitext(self.file.name)[1].lower()
            return ext in ['.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx']
        return False

    @property
    def is_pdf(self):
        if self.file and self.file.name:
            return self.file.name.lower().endswith('.pdf')
        return False


class LiveSession(models.Model):
    PLATFORM_CHOICES = (
        ('meet', 'Google Meet'),
        ('zoom', 'Zoom'),
        ('otro', 'Otro'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_sessions', verbose_name="Curso")
    title = models.CharField(max_length=200, verbose_name="Título de la Sesión")
    description = models.TextField(blank=True, verbose_name="Descripción")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='meet', verbose_name="Plataforma")
    meeting_link = models.URLField(verbose_name="Enlace de la Reunión")
    scheduled_date = models.DateField(verbose_name="Fecha Programada")
    start_time = models.TimeField(verbose_name="Hora de Inicio")
    end_time = models.TimeField(null=True, blank=True, verbose_name="Hora de Fin")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_date', '-start_time']

    @property
    def google_calendar_url(self):
        import urllib.parse
        from django.utils import timezone
        import datetime

        try:
            start_datetime = datetime.datetime.combine(self.scheduled_date, self.start_time)
            tz = timezone.get_current_timezone()
            if timezone.is_naive(start_datetime):
                start_datetime = timezone.make_aware(start_datetime, tz)
            start_utc = start_datetime.astimezone(datetime.timezone.utc)
            
            if self.end_time:
                end_datetime = datetime.datetime.combine(self.scheduled_date, self.end_time)
                if timezone.is_naive(end_datetime):
                    end_datetime = timezone.make_aware(end_datetime, tz)
                end_utc = end_datetime.astimezone(datetime.timezone.utc)
            else:
                end_utc = start_utc + datetime.timedelta(hours=1)
                
            start_str = start_utc.strftime('%Y%m%dT%H%M%SZ')
            end_str = end_utc.strftime('%Y%m%dT%H%M%SZ')
            
            text = urllib.parse.quote(self.title or "Clase en Vivo")
            
            # Construir la descripción
            desc = self.description if self.description else ""
            if self.meeting_link:
                desc += f"\n\nEnlace de la clase: {self.meeting_link}"
                
            details = urllib.parse.quote(desc)
            location = urllib.parse.quote(self.meeting_link or "")
            
            return f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={text}&details={details}&location={location}&dates={start_str}/{end_str}"
        except Exception:
            # Fallback a un enlace simple en caso de que falten fechas
            return "https://calendar.google.com/calendar/render?action=TEMPLATE"

    @property
    def is_finished(self):
        from django.utils import timezone
        import datetime
        now = timezone.localtime(timezone.now())
        
        end_t = self.end_time if self.end_time else (
            datetime.datetime.combine(datetime.date.today(), self.start_time) + datetime.timedelta(hours=1)
        ).time()
        
        dt_end = datetime.datetime.combine(self.scheduled_date, end_t)
        dt_end_aware = timezone.make_aware(dt_end)
        
        return now > dt_end_aware

    def __str__(self):
        return f"{self.title} ({self.scheduled_date})"


# --- MODELOS PARA EXÁMENES ONLINE ---

class Question(models.Model):
    QUESTION_TYPES = (
        ('multiple_choice', 'Opción Múltiple (Autocalificable)'),
        ('text', 'Texto (Desarrollo / Argumentación)'),
        ('file', 'Subida de Archivo'),
    )
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='questions', verbose_name="Examen")
    text = models.TextField(verbose_name="Pregunta")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice', verbose_name="Tipo de Pregunta")
    points = models.DecimalField(max_digits=5, decimal_places=2, default=10, verbose_name="Puntaje")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Pregunta {self.order}: {self.text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name="Pregunta")
    text = models.CharField(max_length=255, verbose_name="Opción")
    is_correct = models.BooleanField(default=False, verbose_name="Es correcta")

    def __str__(self):
        return self.text


class QuestionResponse(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='question_responses', verbose_name="Entrega del Examen")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Pregunta")
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Opción Seleccionada")
    text_answer = models.TextField(blank=True, verbose_name="Respuesta de Texto")
    file_answer = models.FileField(upload_to='submissions/exam_files/', blank=True, null=True, verbose_name="Archivo Adjunto")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Puntaje Obtenido")
    feedback = models.TextField(blank=True, verbose_name="Retroalimentación")

    class Meta:
        unique_together = ('submission', 'question')

    def __str__(self):
        return f"Respuesta a {self.question.id} por {self.submission.student.first_name}"


class QuestionResponseFile(models.Model):
    response = models.ForeignKey(QuestionResponse, on_delete=models.CASCADE, related_name='files', verbose_name="Respuesta")
    file = models.FileField(upload_to='submissions/exam_files/', verbose_name="Archivo Adjunto")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Archivo para pregunta {self.response.question.id}"


class ExamAttempt(models.Model):
    """Registra el intento de un estudiante en un examen online."""
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='exam_attempt', verbose_name="Entrega")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Inicio del Examen")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="Fin del Examen")
    current_question_index = models.PositiveIntegerField(default=0, verbose_name="Pregunta Actual")
    is_completed = models.BooleanField(default=False, verbose_name="Completado")
    question_order = models.JSONField(default=list, blank=True, verbose_name="Orden de Preguntas")
    choice_orders = models.JSONField(default=dict, blank=True, verbose_name="Orden de Opciones")

    def __str__(self):
        return f"Intento de {self.submission.student.first_name} — {self.submission.assignment.title}"


# ============================================================
# ===  NUEVOS RECURSOS DE MÓDULOS (Avisos, Enlaces, Foros) ===
# ============================================================

class ModuleAnnouncement(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='announcements', verbose_name="Módulo")
    title = models.CharField(max_length=200, verbose_name="Título del Aviso")
    content = models.TextField(verbose_name="Contenido")
    publish_date = models.DateTimeField(verbose_name="Fecha de Publicación")
    is_visible = models.BooleanField(default=True, verbose_name="Visible para estudiantes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        ordering = ['-publish_date', '-created_at']

    def __str__(self):
        return self.title


class ModuleLink(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='links', verbose_name="Módulo")
    title = models.CharField(max_length=200, verbose_name="Título del Enlace")
    url = models.URLField(verbose_name="URL")
    is_visible = models.BooleanField(default=True, verbose_name="Visible para estudiantes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title


class ModuleForum(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='forums', verbose_name="Módulo")
    title = models.CharField(max_length=200, verbose_name="Título del Foro")
    content = models.TextField(verbose_name="Contenido del Foro")
    FORUM_TYPES = (
        ('abierto', 'Foro Abierto'),
        ('cerrado', 'Foro Cerrado'),
    )
    forum_type = models.CharField(max_length=20, choices=FORUM_TYPES, default='abierto', verbose_name="Tipo de Foro", help_text="En foros cerrados, el alumno debe responder primero para ver otras respuestas.")
    start_date = models.DateTimeField(verbose_name="Fecha de Inicio")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Cierre")
    is_visible = models.BooleanField(default=True, verbose_name="Visible para estudiantes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        ordering = ['-start_date']
        
    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        if now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True

    def __str__(self):
        return self.title


class ForumReply(models.Model):
    forum = models.ForeignKey(ModuleForum, on_delete=models.CASCADE, related_name='replies', verbose_name="Foro")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='nested_replies', verbose_name="Respuesta Padre")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_replies', verbose_name="Autor")
    content = models.TextField(verbose_name="Respuesta")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Publicación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Edición")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Respuesta de {self.author.first_name} en {self.forum.title}"


class PlatformSetting(models.Model):
    """Modelo Singleton para la configuración global de la plataforma."""
    company_name = models.CharField(max_length=100, default="QHSE Academy", verbose_name="Nombre de la Empresa")
    logo = models.ImageField(upload_to='platform/', blank=True, null=True, verbose_name="Logo de la Empresa")
    primary_color = models.CharField(max_length=20, default="#1B5E37", verbose_name="Color Principal (HEX)", help_text="Opcional. Ej: #1B5E37")
    
    class Meta:
        verbose_name = "Configuración de Plataforma"
        verbose_name_plural = "Configuraciones de Plataforma"

    def save(self, *args, **kwargs):
        # Asegurar que solo exista un registro
        if not self.pk and PlatformSetting.objects.exists():
            return
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Configuración Global"


# ==========================================
# ASISTENCIAS
# ==========================================

class AttendanceRegister(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_registers')
    date = models.DateField(verbose_name="Fecha de Clase")
    description = models.CharField(max_length=200, blank=True, verbose_name="Tema o Descripción")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Asistencia {self.course.title} - {self.date}"

class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('present', 'Presente (P)'),
        ('absent', 'Ausente (A)'),
        ('late', 'Tarde (T)'),
    )
    register = models.ForeignKey(AttendanceRegister, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    observations = models.TextField(blank=True)

    class Meta:
        unique_together = ('register', 'student')

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.get_status_display()} ({self.register.date})"