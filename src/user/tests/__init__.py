import os

from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
setup()
