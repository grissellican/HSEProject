from django.db import transaction
from core.models import (
    SyllabusUnit, Module, Material, Assignment, Question, Choice,
    ModuleLink, ModuleAnnouncement, ModuleForum, Submission
)

@transaction.atomic
def freeze_cohort_content(cohort):
    """
    Creates a static copy of all course resources and binds them to the given cohort.
    This ensures that future edits to the course by the teacher do not affect the
    completed cohort's view.
    """
    course = cohort.course
    
    # 1. Duplicate Syllabus
    for unit in course.syllabus_units.filter(cohort__isnull=True):
        unit_copy = SyllabusUnit.objects.get(id=unit.id)
        unit_copy.pk = None
        unit_copy.cohort = cohort
        unit_copy.save()
        
    old_to_new_module = {}
    old_to_new_assignment = {}
    old_to_new_question = {}
    old_to_new_choice = {}
    
    # 2. Duplicate Modules and their contents
    for module in course.modules.filter(cohort__isnull=True):
        old_module_id = module.id
        
        module_copy = Module.objects.get(id=old_module_id)
        module_copy.pk = None
        module_copy.cohort = cohort
        module_copy.save()
        
        old_to_new_module[old_module_id] = module_copy
        
        old_module = Module.objects.get(id=old_module_id)
        
        # Materials
        for material in old_module.materials.all():
            mat_copy = Material.objects.get(id=material.id)
            mat_copy.pk = None
            mat_copy.module = module_copy
            mat_copy.save()
            
        # Assignments
        for assignment in old_module.assignments.all():
            old_assignment_id = assignment.id
            
            assign_copy = Assignment.objects.get(id=old_assignment_id)
            assign_copy.pk = None
            assign_copy.module = module_copy
            assign_copy.save()
            
            old_to_new_assignment[old_assignment_id] = assign_copy
            
            old_assignment = Assignment.objects.get(id=old_assignment_id)
            
            # Questions
            for question in old_assignment.questions.all():
                old_question_id = question.id
                
                q_copy = Question.objects.get(id=old_question_id)
                q_copy.pk = None
                q_copy.assignment = assign_copy
                q_copy.save()
                
                old_to_new_question[old_question_id] = q_copy
                
                old_question = Question.objects.get(id=old_question_id)
                
                # Choices
                for choice in old_question.choices.all():
                    old_choice_id = choice.id
                    
                    c_copy = Choice.objects.get(id=old_choice_id)
                    c_copy.pk = None
                    c_copy.question = q_copy
                    c_copy.save()
                    
                    old_to_new_choice[old_choice_id] = c_copy
                    
        # ModuleLinks
        for link in old_module.links.all():
            link_copy = ModuleLink.objects.get(id=link.id)
            link_copy.pk = None
            link_copy.module = module_copy
            link_copy.save()
            
        # ModuleAnnouncements (global ones only)
        for ann in old_module.announcements.filter(cohort__isnull=True):
            ann_copy = ModuleAnnouncement.objects.get(id=ann.id)
            ann_copy.pk = None
            ann_copy.module = module_copy
            ann_copy.cohort = cohort
            ann_copy.save()
            
        # ModuleAnnouncements (specific to cohort) -> move to new module
        old_module.announcements.filter(cohort=cohort).update(module=module_copy)
        
        # ModuleForums (global ones only)
        for forum in old_module.forums.filter(cohort__isnull=True):
            forum_copy = ModuleForum.objects.get(id=forum.id)
            forum_copy.pk = None
            forum_copy.module = module_copy
            forum_copy.cohort = cohort
            forum_copy.save()
            
        # ModuleForums (specific to cohort) -> move to new module
        old_module.forums.filter(cohort=cohort).update(module=module_copy)

    # 3. Update Submissions
    submissions = Submission.objects.filter(cohort=cohort)
    for sub in submissions:
        if sub.assignment_id in old_to_new_assignment:
            sub.assignment = old_to_new_assignment[sub.assignment_id]
            sub.save()
            
            # Update QuestionResponses
            for qr in sub.question_responses.all():
                if qr.question_id in old_to_new_question:
                    qr.question = old_to_new_question[qr.question_id]
                    if qr.selected_choice_id and qr.selected_choice_id in old_to_new_choice:
                        qr.selected_choice_id = old_to_new_choice[qr.selected_choice_id].id
                    qr.save()
                    
            # Update ExamAttempt if exists
            if hasattr(sub, 'exam_attempt'):
                attempt = sub.exam_attempt
                if attempt.question_order:
                    attempt.question_order = [
                        old_to_new_question[q_id].id 
                        for q_id in attempt.question_order 
                        if q_id in old_to_new_question
                    ]
                if attempt.choice_orders:
                    new_choice_orders = {}
                    for q_id_str, choices_list in attempt.choice_orders.items():
                        q_id = int(q_id_str)
                        if q_id in old_to_new_question:
                            new_q_id = str(old_to_new_question[q_id].id)
                            new_choices = [
                                old_to_new_choice[c_id].id
                                for c_id in choices_list
                                if c_id in old_to_new_choice
                            ]
                            new_choice_orders[new_q_id] = new_choices
                    attempt.choice_orders = new_choice_orders
                attempt.save()
