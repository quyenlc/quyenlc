import os
import sys
import django

sys.path.append("/Users/quyen.le/git/private/python/django/ams_dev")
os.environ["DJANGO_SETTINGS_MODULE"] = "ams_dev.settings"
django.setup()

from ams.models import User as AmsUser
from django.contrib.auth.models import User
from datetime import datetime

def getFirstName(full_name):
    if (len(full_name.split())<3):
        return user.full_name.split()[-1]
    if full_name.split()[-1].lower() in ('anh','em'):
        return " ".join(full_name.split()[-2:])
    else:
        return user.full_name.split()[-1]

def isSuperUser(role):
    if role == 'admin':
        return 1
    else:
        return 0

users = AmsUser.objects.all()
d_usernames = User.objects.values_list('username', flat=True)

now_t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for user in users:
    if user.username not in d_usernames:
        new_user = User(
                id = user.id,
                username = user.username,
                password = '',
                last_login = now_t,
                is_superuser = isSuperUser(user.role),
                first_name = getFirstName(user.full_name),
                last_name = user.full_name.split()[0],
                email = user.email,
                is_staff = 1,
                is_active = user.flag,
                date_joined = user.created
            )
        new_user.save()
        print(new_user.first_name + " " + new_user.last_name + " : " + new_user.email )
        # break

