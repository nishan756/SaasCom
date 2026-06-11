import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv  # এখানে dotenv ঠিক করা হয়েছে

load_dotenv()

User = get_user_model()

class Command(BaseCommand):  # Django custom command-এর ক্লাস নাম সাধারণত 'Command' হতে হয়
    help = "This will create a superuser if it does not exist"

    def handle(self, *args, **options):
        self.stdout.write("Checking if superuser already exists...")

        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser not found. Now creating superuser...")
            
            username = os.getenv("DJANGO_SUPERUSER_USERNAME")
            email = os.getenv("DJANGO_SUPERUSER_EMAIL")
            password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

            if not username or not password:
                self.stdout.write(self.style.ERROR("Error: Env variables for username or password missing!"))
                return

            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Successfully created superuser."))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists."))
        
        
    