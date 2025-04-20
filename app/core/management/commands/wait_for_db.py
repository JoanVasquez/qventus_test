# 🔄 Import required libraries
import time
import psycopg2
from psycopg2 import OperationalError
from django.core.management.base import BaseCommand
import os


# 🛠️ Command class for database connection check
class Command(BaseCommand):
    # 💡 Command description
    help = 'Waits for the PostgreSQL database to be available.'

    # ⚙️ Main handler method
    def handle(self, *args, **options):
        # 🖨️ Print initial status message
        self.stdout.write('Waiting for database...')
        while True:
            try:
                # 🔌 Attempt database connection
                conn = psycopg2.connect(
                    dbname=os.getenv("POSTGRES_DB"),
                    user=os.getenv("POSTGRES_USER"),
                    password=os.getenv("POSTGRES_PASSWORD"),
                    host=os.getenv("POSTGRES_HOST", "db"),
                    port=5432,
                )
                # 🔒 Close connection if successful
                conn.close()
                break
            except OperationalError:
                # ⏳ If connection fails, wait and retry
                self.stdout.write('.', ending='')
                self.stdout.flush()
                time.sleep(1)
        # ✅ Print success message when database is ready
        self.stdout.write(self.style.SUCCESS('Database is ready!'))
