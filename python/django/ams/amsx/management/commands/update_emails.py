from django.core.management.base import BaseCommand, CommandError
from amsx.utils import Google
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):

    def handle(self, *args, **options):
        # ... Should run migrate_users before
        self.stdout.write(self.style.SUCCESS("Start ..."), ending='\n')
        service_account_file = 'amsx/.credentials/Infra-Infosec-378d3f89c912.json'
        SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets.readonly', #Must be included although is not granted by Super Administrators
        ]
        tmp_session = Google(SCOPES, service_account_file)
        spreadsheetId = '1L2SKvA6VdaLvYFAUeFGHyPfp4LQWQSzCZvnriA9KNDQ'
        rangeName = 'AMSUsers!A2:B'
        sheet_data = tmp_session.readSheet(spreadsheetId, rangeName)
        if sheet_data['return_code'] != 200:
            print("Could read spreadsheet. Detail: " + str(sheet_data['message']) + ". Error code:" + str(sheet_data['return_code']))
            return None
        values = sheet_data['values']
        for row in values:
            user_name = row[0]
            new_email = ''
            if len(row) > 1:
                new_email = row[1]
            try:
                auth_user = User.objects.get(username__exact = user_name)
                if new_email != '':
                    self.stdout.write(self.style.SUCCESS("Update email for user " + user_name))
                    auth_user.email = new_email
                    auth_user.save()
            except ObjectDoesNotExist as e:
                self.stdout.write(self.style.NOTICE("User " + user_name + " does not exist !!!"))



