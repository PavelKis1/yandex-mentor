import os
import shutil

templates_dir = r'c:\Users\Pavel\Desktop\yandex_review\scripts\archive\lecture_templates'
tasks_dir = r'c:\Users\Pavel\Desktop\yandex_review\backend\tasks'

for dir_name in os.listdir(tasks_dir):
    if len(dir_name) >= 2 and dir_name[0:2].isdigit():
        template_path = os.path.join(templates_dir, dir_name + '.md')
        target_path = os.path.join(tasks_dir, dir_name, 'lecture.md')
        
        if os.path.exists(template_path):
            shutil.copyfile(template_path, target_path)
            print(f'Applied {dir_name}.md to {target_path}')
        else:
            print(f'Template not found: {template_path}')
