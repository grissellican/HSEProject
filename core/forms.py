from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import User, Course, Module, Material, Assignment, Submission, LiveSession

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50/50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm'}),
        required=False,
        label="Contraseña",
        help_text="Dejar en blanco si solo está editando y no desea cambiarla."
    )

    class Meta:
        model = User
        fields = ['first_name', 'lastname', 'email', 'phone', 'role', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm'}),
            'lastname': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm'}),
            'email': forms.EmailInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm'}),
            'phone': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm'}),
            'role': forms.Select(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-[#2b3494] focus:ring-[#2b3494] h-5 w-5'}),
        }


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'presentation', 'show_phone']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-[#38657f]/10 file:text-[#38657f] hover:file:bg-[#38657f]/20 cursor-pointer'
            }),
            'presentation': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='extends'),
            'show_phone': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-[#38657f] focus:ring-[#38657f] h-5 w-5'
            }),
        }


class CourseForm(forms.ModelForm):
    # Campos personalizados para filtrar los roles en el formulario CRUD
    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(role='teacher', is_active=True),
        required=False,
        label="Docente a Cargo",
        widget=forms.Select(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm'}),
        empty_label="-- Seleccionar Docente Asignado --"
    )
    
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='student', is_active=True),
        required=False,
        label="Alumnos Matriculados",
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Course
        fields = ['title', 'category', 'welcome_description', 'cover_image', 'image_url', 'start_date', 'teacher', 'students', 'is_active', 'capacities', 'allow_teacher_edit_syllabus']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm', 'placeholder': 'Ej. Curso de Primeros Auxilios'}),
            'category': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm', 'placeholder': 'Ej. Seguridad Industrial'}),
            'welcome_description': CKEditor5Widget(config_name='default'),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 text-sm'}),
            'image_url': forms.URLInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm', 'placeholder': 'https://ejemplo.com/imagen.jpg'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-[#2b3494] focus:ring-[#2b3494] h-5 w-5'}),
            
            'capacities': CKEditor5Widget(config_name='default'),
            'allow_teacher_edit_syllabus': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-[#2b3494] focus:ring-[#2b3494] h-5 w-5'}),
        }


# ========== FORMULARIOS DEL DOCENTE ==========

_input_cls = 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm'
_textarea_cls = _input_cls + ' min-h-[100px]'
_check_cls = 'rounded border-gray-300 text-[#2b3494] focus:ring-[#2b3494] h-5 w-5'

class SyllabusTeacherForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['syllabus_introduction', 'syllabus_objectives']
        widgets = {
            'syllabus_introduction': CKEditor5Widget(config_name='default'),
            'syllabus_objectives': CKEditor5Widget(config_name='default'),
        }

from .models import SyllabusUnit
from django.forms import inlineformset_factory

class SyllabusUnitForm(forms.ModelForm):
    class Meta:
        model = SyllabusUnit
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full rounded-md border border-gray-300 px-3 py-2 bg-white focus:border-[#38657f] focus:ring-1 focus:ring-[#38657f] text-sm flex-1', 'placeholder': 'Ej. Introducción a Node.js'}),
            'order': forms.NumberInput(attrs={'class': 'w-16 rounded-md border border-gray-300 px-2 py-2 bg-white focus:border-[#38657f] focus:ring-1 focus:ring-[#38657f] text-sm text-center'}),
        }

SyllabusUnitFormSet = inlineformset_factory(Course, SyllabusUnit, form=SyllabusUnitForm, extra=1, can_delete=True)

class EvaluationSystemTeacherForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['evaluation_system_description']
        widgets = {
            'evaluation_system_description': CKEditor5Widget(config_name='default'),
        }

from .models import EvaluationImage
class EvaluationImageForm(forms.ModelForm):
    class Meta:
        model = EvaluationImage
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm', 'placeholder': 'Ej. Rúbrica 1'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 text-sm'}),
            'order': forms.NumberInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-2 bg-gray-50 focus:border-[#2b3494] focus:ring-1 focus:ring-[#2b3494] text-sm', 'min': 0, 'value': 0}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order', 'is_visible']
        widgets = {
            'title': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Ej. Módulo 1 — Introducción'}),
            'description': forms.Textarea(attrs={'class': _textarea_cls, 'rows': 3, 'placeholder': 'Descripción del módulo...'}),
            'order': forms.NumberInput(attrs={'class': _input_cls, 'min': 0}),
            'is_visible': forms.CheckboxInput(attrs={'class': _check_cls}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'description', 'file', 'material_type', 'is_visible']
        widgets = {
            'title': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Ej. Guía de Seguridad Industrial'}),
            'description': CKEditor5Widget(config_name='default'),
            'file': forms.ClearableFileInput(attrs={'class': _input_cls}),
            'material_type': forms.Select(attrs={'class': _input_cls}),
            'is_visible': forms.CheckboxInput(attrs={'class': _check_cls}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'delivery_specifications', 'evaluation_criteria', 'attached_file', 'assignment_type', 'due_date', 'max_score', 'max_attempts', 'is_visible']
        widgets = {
            'title': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Ej. Análisis de Riesgos Laborales'}),
            'description': CKEditor5Widget(config_name='extends'),
            'delivery_specifications': CKEditor5Widget(config_name='extends'),
            'evaluation_criteria': CKEditor5Widget(config_name='extends'),
            'attached_file': forms.ClearableFileInput(attrs={'class': _input_cls}),
            'assignment_type': forms.Select(attrs={'class': _input_cls}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': _input_cls}),
            'max_score': forms.NumberInput(attrs={'class': _input_cls, 'min': 1, 'step': '0.01'}),
            'max_attempts': forms.NumberInput(attrs={'class': _input_cls, 'min': 0, 'step': '1'}),
            'is_visible': forms.CheckboxInput(attrs={'class': _check_cls}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={'class': _input_cls, 'min': 0, 'step': '0.01', 'placeholder': 'Ej. 85.5'}),
            'feedback': forms.Textarea(attrs={'class': _textarea_cls, 'rows': 3, 'placeholder': 'Retroalimentación para el estudiante...'}),
        }

    def __init__(self, *args, max_score=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].widget.attrs['max'] = max_score
        self.fields['score'].label = f"Calificación (máx. {max_score})"
        self.max_score_val = max_score

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is not None and self.max_score_val is not None:
            if score > float(self.max_score_val):
                from django.core.exceptions import ValidationError
                raise ValidationError(f"La calificación no puede ser mayor a {self.max_score_val}.")
        return score


class LiveSessionForm(forms.ModelForm):
    class Meta:
        model = LiveSession
        fields = ['title', 'description', 'platform', 'meeting_link', 'scheduled_date', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Ej. Clase 1 — Normativa de Seguridad'}),
            'description': forms.Textarea(attrs={'class': _textarea_cls, 'rows': 2, 'placeholder': 'Tema a tratar en la sesión...'}),
            'platform': forms.Select(attrs={'class': _input_cls}),
            'meeting_link': forms.URLInput(attrs={'class': _input_cls, 'placeholder': 'https://meet.google.com/xxx-xxx-xxx'}),
            'scheduled_date': forms.DateInput(attrs={'type': 'date', 'class': _input_cls}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': _input_cls}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': _input_cls}),
        }


# --- FORMULARIOS PARA EXÁMENES ONLINE ---

from .models import Question, Choice, QuestionResponse

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'points', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'class': _textarea_cls, 'rows': 2, 'placeholder': 'Escriba la pregunta aquí...'}),
            'question_type': forms.Select(attrs={'class': _input_cls, 'id': 'id_question_type'}),
            'points': forms.NumberInput(attrs={'class': _input_cls, 'min': 0, 'step': '0.01'}),
            'order': forms.NumberInput(attrs={'class': _input_cls, 'min': 0}),
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Opción de respuesta...'}),
            'is_correct': forms.CheckboxInput(attrs={'class': _check_cls}),
        }

class QuestionGradeForm(forms.ModelForm):
    class Meta:
        model = QuestionResponse
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={'class': _input_cls, 'min': 0, 'step': '0.01', 'placeholder': 'Ej. 10.0'}),
            'feedback': forms.Textarea(attrs={'class': _textarea_cls, 'rows': 2, 'placeholder': 'Comentarios opcionales sobre esta respuesta...'}),
        }

    def __init__(self, *args, max_score=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].widget.attrs['max'] = max_score
        self.fields['score'].label = f"Puntaje (máx. {max_score})"


# --- FORMULARIOS DE NUEVOS RECURSOS (Avisos, Enlaces, Foros) ---

from .models import ModuleAnnouncement, ModuleLink, ModuleForum, ForumReply
from django_ckeditor_5.widgets import CKEditor5Widget

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = ModuleAnnouncement
        fields = ['title', 'content', 'publish_date', 'is_visible']
        widgets = {
            'title': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Título del aviso...'}),
            'content': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='default'),
            'publish_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': _input_cls}),
            'is_visible': forms.CheckboxInput(attrs={'class': _check_cls}),
        }

class LinkForm(forms.ModelForm):
    class Meta:
        model = ModuleLink
        fields = ['title', 'url', 'is_visible']
        widgets = {
            'title': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Título del enlace...'}),
            'url': forms.URLInput(attrs={'class': _input_cls, 'placeholder': 'https://...'}),
            'is_visible': forms.CheckboxInput(attrs={'class': _check_cls}),
        }

class ForumForm(forms.ModelForm):
    class Meta:
        model = ModuleForum
        fields = ['title', 'content', 'forum_type', 'start_date', 'end_date', 'is_visible']
        widgets = {
            'title': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Título del foro...'}),
            'content': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='default'),
            'forum_type': forms.Select(attrs={'class': _input_cls}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': _input_cls}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': _input_cls}),
            'is_visible': forms.CheckboxInput(attrs={'class': _check_cls}),
        }

class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['content']
        widgets = {
            'content': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='default'),
        }

class ExamTextAnswerForm(forms.Form):
    text_answer = forms.CharField(
        widget=CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='extends'),
        required=False,
        label=""
    )

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def to_python(self, data):
        if not data:
            return []
        return data
    
    def clean(self, data, initial=None):
        if not data and self.required:
            from django.core.exceptions import ValidationError
            raise ValidationError(self.error_messages['required'], code='required')
        return data

# --- FORMULARIOS DEL ESTUDIANTE ---

class StudentSubmissionForm(forms.ModelForm):
    """Formulario para que el estudiante suba su entrega (archivo + comentario)."""
    file = MultipleFileField(
        widget=MultipleFileInput(attrs={
            'class': 'hidden',
            'id': 'dropzone-file-input',
            'multiple': True,
        }),
        required=False,
        label='Archivo de Entrega'
    )
    
    class Meta:
        model = Submission
        fields = ['text_content']
        widgets = {
            'text_content': forms.Textarea(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 bg-gray-50 focus:border-[#38657f] focus:ring-1 focus:ring-[#38657f] text-sm',
                'rows': 4,
                'placeholder': 'Escribe un comentario sobre tu entrega (opcional)...',
            }),
        }
        labels = {
            'text_content': 'Comentario de Entrega',
        }