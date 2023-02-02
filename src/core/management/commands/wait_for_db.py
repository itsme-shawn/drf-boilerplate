"""
Django command to wait for the db to be available
"""
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OperationalError


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Waiting for database...")
        db_up = False
        check_count = 0
        while db_up is False:
            if check_count > 20:
                self.stdout.write(self.style.ERROR("Database refused connection"))
                return
            try:
                self.check(databases=["default"])  # type: ignore
                db_up = True
            except (Psycopg2OperationalError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)
                check_count += 1

        self.stdout.write(self.style.SUCCESS("Database available!"))
