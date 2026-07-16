from core.models import User, Assignment, Submission, ExamAttempt

existing = Submission.objects.filter(assignment__assignment_type='examen_online').first()
print('Existing:', existing)
print('Hasattr:', hasattr(existing, 'exam_attempt'))
if hasattr(existing, 'exam_attempt'):
    try:
        existing.exam_attempt.delete()
        print('Deleted old attempt')
    except Exception as e:
        print('Delete Error:', e)

try:
    ExamAttempt.objects.create(submission=existing, current_question_index=0)
    print('Created new attempt')
except Exception as e:
    print('Create Error:', type(e), e)
