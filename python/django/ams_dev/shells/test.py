import os
import sys
import django

sys.path.append("/Users/quyen.le/git/private/python/django/ams_dev")
os.environ["DJANGO_SETTINGS_MODULE"] = "ams_dev.settings"
django.setup()

from ams.models import Location
locations = Location.objects.all()
for location in locations:
    print(location)