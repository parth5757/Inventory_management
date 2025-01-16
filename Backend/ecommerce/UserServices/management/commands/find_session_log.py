from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = 'List all the session log'

    def handle(self, *args, **options):
        sessions = Session.objects.all()
        if not sessions:
            self.stdout.write("No sessions found")
            return
        
        for session in sessions:
            session_data = session.get_decoded()
            self.stdout.write(f"Session Key: {session.session_key}")
            self.stdout.write(f"Session Value: {session.session_data}")
            self.stdout.write("_" * 50)