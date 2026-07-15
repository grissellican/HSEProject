import re
with open('z:/proyectos/PythonProjects/HSEProject-main/templates/dashboards/teacher/teacher_attendance_upload.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_text = re.sub(r'</div>\s*</main>\s*</div>\s*<div class="mb-8 flex items-center justify-between" id="modulos">.*', '</div>\n        </main>\n    </div>\n</body>\n</html>', text, flags=re.DOTALL)

with open('z:/proyectos/PythonProjects/HSEProject-main/templates/dashboards/teacher/teacher_attendance_upload.html', 'w', encoding='utf-8') as f:
    f.write(new_text)
