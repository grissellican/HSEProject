import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hse_canvas_project.settings')
django.setup()

from django.test import Client
from core.models import User, Assignment, Submission, ExamAttempt
import traceback

def run_test():
    client = Client()
    
    # 1. Get the first student and exam
    student = User.objects.filter(role='student').first()
    assignment = Assignment.objects.filter(assignment_type='examen_online').first()
    
    if not student or not assignment:
        print("Missing student or assignment")
        return
        
    print(f"Testing with student {student.username} and assignment {assignment.id}")
    client.force_login(student)
    
    # Generate an existing submission and completed attempt
    existing = Submission.objects.filter(assignment=assignment, student=student).first()
    if not existing:
        existing = Submission.objects.create(assignment=assignment, student=student, attempts=1)
        ExamAttempt.objects.create(submission=existing, is_completed=True)
    
    # 2. Try POSTing to the view
    print("Sending POST request to student_exam_start...")
    try:
        response = client.post(f'/student/examen/{assignment.id}/empezar/')
        print(f"Response status: {response.status_code}")
    except Exception as e:
        print("Exception caught during POST:")
        traceback.print_exc()
        
run_test()
