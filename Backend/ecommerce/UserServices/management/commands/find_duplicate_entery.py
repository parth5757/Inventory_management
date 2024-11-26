from django.core.management.base import BaseCommand
from django.db.models import Count
from UserServices.models import Users

class Command(BaseCommand):
    help = 'Find duplicate phone numbers or users by name in the Users model'

    def handle(self, *args, **options):
        duplicate_numbers = Users.objects.values('phone').annotate(count=Count('phone')).filter(count__gt=1)
        print(duplicate_numbers)

        for number in duplicate_numbers:
            self.stdout.write(self.style.SUCCESS(f"Phone number: {number['phone']}, Count: {number['count']}"))

        self.find_users_by_name()

    def find_users_by_name(self):
        print("Finding users by name...")
        users = Users.objects.filter(username__icontains='parth')
        for user in users:
            self.stdout.write(self.style.SUCCESS(f"User name: {user.username}"))