from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from datetime import datetime  


class Command(BaseCommand):

    def handle(self, *args, **options):
        # ...
        self.stdout.write(self.style.SUCCESS("Start ..."), ending='\n')
        now = datetime.now()
        for user in User.objects.raw('SELECT * from users'):
            try:
                auth_user = User.objects.get(username__exact = user.username)
                # self.stdout.write(self.style.WARNING("Update info for user "), ending = ''); self.stdout.write(self.style.SUCCESS(user.username))
                if user.new_email != None:
                    auth_user.email = user.new_email
                else:
                    auth_user.email = user.email
                print(str(auth_user.id) + ": "+ auth_user.username + " - " + str(user.id) + ": " + user.username)
                auth_user.date_joined = now
                auth_user.last_login = now
                auth_user.save()

            except ObjectDoesNotExist as e:
                self.stdout.write(self.style.WARNING("User "), ending = '')
                self.stdout.write(self.style.SUCCESS(user.username), ending = '')
                self.stdout.write(self.style.WARNING(" does not exist. Prepare to create new one ..."))
                new_user = User(id = user.id, username=user.username, email = user.email, date_joined = now, last_login = user.modified)
                new_user.save()
