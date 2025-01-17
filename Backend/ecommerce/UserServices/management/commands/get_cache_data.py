from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Fetches all cache keys and their values.'

    def handle(self, *args, **kwargs):
        try:
            keys = cache.keys('*')  # Fetch all cache keys
            if not keys:
                self.stdout.write(self.style.WARNING('No cache keys found.'))
                return

            all_cache_data = {key: cache.get(key) for key in keys}
            for key, value in all_cache_data.items():
                self.stdout.write(f"{key}: {value}")
            
            self.stdout.write(self.style.SUCCESS('Cache data fetched successfully!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error retrieving cache data: {str(e)}"))
