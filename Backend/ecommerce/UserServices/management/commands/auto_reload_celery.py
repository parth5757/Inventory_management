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

class Command(BaseCommand):
    help = 'Starts the Celery worker with auto-reload on code changes.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting Celery worker with auto-reload')
        autoreload.run_with_reloader(restart_celery)


#celery command to run

# celery -A ecommerce.celery worker --pool=solo -l info0