# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards por Roles
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    
    # Shared Course Routes
    path('curso/<int:course_id>/syllabus/', views.course_syllabus, name='course_syllabus'),
    path('curso/<int:course_id>/evaluacion/', views.course_evaluation, name='course_evaluation'),

    # Dashboards por Roles (Añade estas líneas)
    path('admin/dashboard/', views.admin_panel_general, name='admin_panel_general'),
    path('admin/usuarios/', views.admin_section_users, name='admin_usuarios'),
    path('admin/docentes/', views.admin_section_teachers, name='admin_docentes'),
    path('admin/estudiantes/', views.admin_section_students, name='admin_estudiantes'),
    path('admin/cursos/', views.admin_section_courses, name='admin_cursos'),
    path('admin/configuracion/', views.admin_platform_settings, name='admin_platform_settings'),
    
    # Asistencias para Admin
    path('admin/asistencias/', views.admin_attendance_reports, name='admin_attendance_reports'),
    path('admin/asistencias/curso/<int:course_id>/', views.admin_attendance_course_detail, name='admin_attendance_course_detail'),
    path('admin/asistencias/estudiante/<int:student_id>/', views.admin_attendance_student_detail, name='admin_attendance_student_detail'),

    # Acciones CRUD - Cuentas de Usuarios
    path('admin/usuarios/nuevo/', views.user_create, name='user_create_generic'),
    path('admin/usuarios/nuevo/<str:target_role>/', views.user_create, name='user_create_role'),
    path('admin/usuarios/editar/<int:pk>/', views.user_update, name='user_update'),
    path('admin/usuarios/eliminar/<int:pk>/', views.user_delete, name='user_delete'),

    # Acciones CRUD - Cursos
    path('admin/cursos/nuevo/', views.course_create, name='course_create'),
    path('admin/cursos/editar/<int:pk>/', views.course_update, name='course_update'),
    path('admin/cursos/eliminar/<int:pk>/', views.course_delete, name='course_delete'),
    
    # Sílabo y Evaluación para Admin
    path('admin/curso/<int:course_id>/syllabus/editar/', views.admin_edit_syllabus, name='admin_edit_syllabus'),
    path('admin/curso/<int:course_id>/evaluacion/editar/', views.admin_edit_evaluation, name='admin_edit_evaluation'),
    path('admin/evaluacion-imagen/<int:image_id>/eliminar/', views.admin_evaluation_image_delete, name='admin_evaluation_image_delete'),

    # Cohortes (Ciclo de vida de cursos)
    path('admin/curso/<int:course_id>/cohortes/', views.admin_course_cohorts, name='admin_course_cohorts'),
    path('admin/cohorte/crear/<int:course_id>/', views.admin_cohort_create, name='admin_cohort_create'),
    path('admin/cohorte/<int:cohort_id>/cerrar/', views.admin_cohort_close, name='admin_cohort_close'),
    path('admin/cohorte/<int:cohort_id>/', views.admin_cohort_detail, name='admin_cohort_detail'),

    # ========== RUTAS DEL DOCENTE ==========
    
    # Perfil Docente
    path('teacher/perfil/', views.teacher_profile, name='teacher_profile'),
    
    # Detalle de curso
    path('teacher/curso/<int:course_id>/', views.teacher_course_detail, name='teacher_course_detail'),
    path('teacher/curso/<int:course_id>/syllabus/editar/', views.teacher_edit_syllabus, name='teacher_edit_syllabus'),
    path('teacher/curso/<int:course_id>/evaluacion/editar/', views.teacher_edit_evaluation, name='teacher_edit_evaluation'),
    path('teacher/evaluacion-imagen/<int:image_id>/eliminar/', views.teacher_evaluation_image_delete, name='teacher_evaluation_image_delete'),
    
    # Módulos
    path('teacher/curso/<int:course_id>/modulo/nuevo/', views.teacher_module_create, name='teacher_module_create'),
    path('teacher/modulo/<int:module_id>/editar/', views.teacher_module_update, name='teacher_module_update'),
    path('teacher/modulo/<int:module_id>/eliminar/', views.teacher_module_delete, name='teacher_module_delete'),
    path('teacher/modulo/<int:module_id>/toggle/', views.teacher_module_toggle_visibility, name='teacher_module_toggle_visibility'),
    
    # Materiales
    path('teacher/modulo/<int:module_id>/material/nuevo/', views.teacher_material_create, name='teacher_material_create'),
    path('teacher/material/<int:material_id>/detalle/', views.teacher_material_detail, name='teacher_material_detail'),
    path('teacher/material/<int:material_id>/eliminar/', views.teacher_material_delete, name='teacher_material_delete'),
    path('teacher/material/<int:material_id>/toggle/', views.teacher_material_toggle_visibility, name='teacher_material_toggle_visibility'),
    
    # Avisos
    path('teacher/modulo/<int:module_id>/aviso/nuevo/', views.teacher_announcement_create, name='teacher_announcement_create'),
    path('teacher/aviso/<int:pk>/editar/', views.teacher_announcement_update, name='teacher_announcement_update'),
    path('teacher/aviso/<int:pk>/eliminar/', views.teacher_announcement_delete, name='teacher_announcement_delete'),
    path('teacher/aviso/<int:pk>/toggle/', views.teacher_announcement_toggle_visibility, name='teacher_announcement_toggle_visibility'),

    # Enlaces
    path('teacher/modulo/<int:module_id>/enlace/nuevo/', views.teacher_link_create, name='teacher_link_create'),
    path('teacher/enlace/<int:pk>/editar/', views.teacher_link_update, name='teacher_link_update'),
    path('teacher/enlace/<int:pk>/eliminar/', views.teacher_link_delete, name='teacher_link_delete'),
    path('teacher/enlace/<int:pk>/toggle/', views.teacher_link_toggle_visibility, name='teacher_link_toggle_visibility'),

    # Foros
    path('teacher/modulo/<int:module_id>/foro/nuevo/', views.teacher_forum_create, name='teacher_forum_create'),
    path('teacher/foro/<int:pk>/editar/', views.teacher_forum_update, name='teacher_forum_update'),
    path('teacher/foro/<int:pk>/eliminar/', views.teacher_forum_delete, name='teacher_forum_delete'),
    path('teacher/foro/<int:pk>/toggle/', views.teacher_forum_toggle_visibility, name='teacher_forum_toggle_visibility'),
    path('teacher/foro/<int:pk>/detalle/', views.teacher_forum_detail, name='teacher_forum_detail'),
    path('teacher/foro/respuesta/<int:reply_id>/eliminar/', views.teacher_forum_reply_delete, name='teacher_forum_reply_delete'),
    
    # Tareas y Evaluaciones
    path('teacher/modulo/<int:module_id>/tarea/nueva/', views.teacher_assignment_create, name='teacher_assignment_create'),
    path('teacher/tarea/<int:assignment_id>/editar/', views.teacher_assignment_update, name='teacher_assignment_update'),
    path('teacher/tarea/<int:assignment_id>/eliminar/', views.teacher_assignment_delete, name='teacher_assignment_delete'),
    path('teacher/tarea/<int:assignment_id>/toggle/', views.teacher_assignment_toggle_visibility, name='teacher_assignment_toggle_visibility'),
    
    # Entregas y Calificaciones
    path('teacher/tarea/<int:assignment_id>/entregas/', views.teacher_assignment_submissions, name='teacher_assignment_submissions'),
    path('teacher/entrega/<int:submission_id>/calificar/', views.teacher_grade_submission, name='teacher_grade_submission'),
    
    # Clases en Vivo
    path('teacher/curso/<int:course_id>/sesion/nueva/', views.teacher_live_session_create, name='teacher_live_session_create'),
    path('teacher/sesion/<int:session_id>/editar/', views.teacher_live_session_update, name='teacher_live_session_update'),
    path('teacher/sesion/<int:session_id>/eliminar/', views.teacher_live_session_delete, name='teacher_live_session_delete'),
    
    # Estudiantes, Calificaciones y Asistencias
    path('teacher/curso/<int:course_id>/estudiantes/', views.teacher_students_list, name='teacher_students_list'),
    path('teacher/curso/<int:course_id>/estudiante/<int:student_id>/notas/', views.teacher_student_grades_detail, name='teacher_student_grades_detail'),
    path('teacher/curso/<int:course_id>/asistencias/', views.teacher_attendance_upload, name='teacher_attendance_upload'),
    path('teacher/curso/<int:course_id>/asistencias/plantilla/', views.teacher_download_attendance_template, name='teacher_download_attendance_template'),
    
    # Exámenes Online
    path('teacher/examen/<int:assignment_id>/preguntas/', views.teacher_exam_questions, name='teacher_exam_questions'),
    path('teacher/examen/<int:assignment_id>/pregunta/nueva/', views.teacher_question_create, name='teacher_question_create'),
    path('teacher/pregunta/<int:question_id>/editar/', views.teacher_question_update, name='teacher_question_update'),
    path('teacher/pregunta/<int:question_id>/eliminar/', views.teacher_question_delete, name='teacher_question_delete'),
    
    path('teacher/pregunta/<int:question_id>/opcion/nueva/', views.teacher_choice_create, name='teacher_choice_create'),
    path('teacher/opcion/<int:choice_id>/eliminar/', views.teacher_choice_delete, name='teacher_choice_delete'),

    # ========== RUTAS DEL ESTUDIANTE ==========
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/calificaciones/', views.student_grades, name='student_grades'),
    path('student/pendientes/', views.student_pending, name='student_pending'),
    path('student/archivos/', views.student_files, name='student_files'),
    
    # Curso
    path('student/curso/<int:course_id>/', views.student_course_home, name='student_course_home'),
    path('student/curso/<int:course_id>/docente/', views.student_course_teacher, name='student_course_teacher'),
    path('student/curso/<int:course_id>/clases/', views.student_course_live, name='student_course_live'),
    path('student/curso/<int:course_id>/modulos/', views.student_course_modules, name='student_course_modules'),
    
    # Items de contenido
    path('student/material/<int:material_id>/', views.student_material_detail, name='student_material_detail'),
    path('student/aviso/<int:announcement_id>/', views.student_announcement_detail, name='student_announcement_detail'),
    path('student/foro/<int:forum_id>/', views.student_forum_detail, name='student_forum_detail'),
    path('student/foro/respuesta/<int:reply_id>/editar/', views.student_forum_reply_edit, name='student_forum_reply_edit'),
    path('student/tarea/<int:assignment_id>/', views.student_assignment_detail, name='student_assignment_detail'),
    path('student/tarea/<int:assignment_id>/entregar/', views.student_submit_assignment, name='student_submit_assignment'),
    path('student/evaluacion/<int:assignment_id>/', views.student_evaluation_detail, name='student_evaluation_detail'),
    path('student/evaluacion/<int:assignment_id>/aceptar/', views.student_evaluation_accept, name='student_evaluation_accept'),
    path('student/examen/<int:assignment_id>/', views.student_exam_detail, name='student_exam_detail'),
    path('student/examen/<int:assignment_id>/empezar/', views.student_exam_start, name='student_exam_start'),
    path('student/examen/<int:assignment_id>/todo/', views.student_exam_all, name='student_exam_all'),
    path('student/examen/<int:assignment_id>/pregunta/<int:q>/', views.student_exam_question, name='student_exam_question'),
    path('student/examen/<int:assignment_id>/finalizar/', views.student_exam_finish, name='student_exam_finish'),
]
