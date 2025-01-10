import os
import shlex
import subprocess
from django.core.management.base import BaseCommand
from django.utils import autoreload

def restart_celery():
    # Terminate existing Celery worker process
    terminate_cmd = 'taskkill /F /IM celery.exe'
    subprocess.call(shlex.split(terminate_cmd), shell=True)

    # Start a new Celery worker
    start_cmd = 'celery -A ecommerce.celery worker --pool=solo -l info'
    subprocess.call(shlex.split(start_cmd), shell=True)

def monitor_and_reload():
    # Files to watch for changes
    file_paths = [
        os.path.join('ecommerce', 'celery.py'),
        os.path.join('ecommerce', 'settings', 'base.py'),
        os.path.join('ecommerce', 'settings', 'local.py'),
        os.path.join('ecommerce', 'settings', 'production.py')
    ]

    # Find all `tasks.py` files in the project directory
    for root, dirs, files in os.walk('.'):  # '.' represents the project root
        for file in files:
            if file == 'tasks.py':
                file_paths.append(os.path.join(root, file))

    print("Monitoring these files for changes:")
    for file_path in file_paths:
        print(f"- {file_path}")

    # Monitor the files for changes
    autoreload.run_with_reloader(lambda: restart_celery_if_changed(file_paths))

def restart_celery_if_changed(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path) and os.path.getmtime(file_path):
            print(f"Detected change in: {file_path}")
            restart_celery()
            break

class Command(BaseCommand):
    help = 'Starts the Celery worker with auto-reload on code changes.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting Celery worker with auto-reload')
        monitor_and_reload()



#celery command to run

# celery -A ecommerce.celery worker --pool=solo -l info0