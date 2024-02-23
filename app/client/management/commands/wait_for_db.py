import time 

from psycopg import OperationalError as PsycopgOpError

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgOpError, OperationalError):
                self.stdout.write("Database unavailable, wait a second...")
                time.sleep(1)

        self.stdout.write("Database is up to date!")
