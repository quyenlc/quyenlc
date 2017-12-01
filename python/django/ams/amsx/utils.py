from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from google.auth.exceptions import RefreshError
import json

class Google(object):
    """docstring for Google"""
    def __init__(self, scopes, service_account_file = None, subject = 'pvn_kpi_sys@punch.vn'):
        super(Google, self).__init__()
        self.service_account_file = service_account_file
        self.scopes = scopes
        self.subject = subject

        """http://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html"""
        if service_account_file != None:
            delegated_credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes = scopes, subject = subject)
            self.session = AuthorizedSession(delegated_credentials)
            basic_credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes = scopes)
            self.basic_session = AuthorizedSession(basic_credentials)

    def get_users(self):
        ouput = {}
        ouput['users']  = []
        initial_request = 'https://www.googleapis.com/admin/directory/v1/users?domain=punch.vn&projection=basic&orderBy=email'
        request         = 'https://www.googleapis.com/admin/directory/v1/users?domain=punch.vn&projection=basic&orderBy=email' 
        has_next_page = True
        while has_next_page :
            try:
                response = self.session.request('GET', request)
            except RefreshError as e:
                ouput['return_code']    = 500
                ouput['message']        = str(e)
                return ouput

            result = vars(response)
            users = json.loads(result['_content'])
            if 'error' in users:
                ouput['return_code']    = users['error']['code']
                ouput['message']        = users['error']['message']
                return ouput
            else:
                ouput['return_code']    = 200
                ouput['users']          = ouput['users'] + users['users']
            if not 'nextPageToken' in users:
                has_next_page = False
            else:
                # print("Next Page Token: " + users['nextPageToken'])
                request = initial_request + "&pageToken=" + users['nextPageToken']
        return ouput

    def get_tokens(self, email):
        ouput = {}
        try:
            response = self.session.request('GET', 'https://www.googleapis.com/admin/directory/v1/users/' + email + '/tokens')
        except RefreshError as e:
            ouput['return_code']    = 500
            ouput['message']        = str(e)
            return ouput

        result = vars(response)
        tokens = json.loads(result['_content'])
        if 'error' in tokens:
            ouput['return_code']    = tokens['error']['code']
            ouput['message']        = tokens['error']['message']
            return ouput
        else:
            ouput['return_code']    = 200
            ouput['tokens']         = tokens['items']
            return ouput
        
    def readSheet(self, sheetId, sheetRange):
        ouput = {}
        try:
            response = self.basic_session.request('GET', 'https://sheets.googleapis.com/v4/spreadsheets/'+ sheetId +'/values/'+ sheetRange)
        except RefreshError as e:
            ouput['return_code']    = 500
            ouput['message']        = str(e)
            return ouput

        result = vars(response)
        data = json.loads(result['_content'])

        if 'error' in data:
            ouput['return_code']    = data['error']['code']
            ouput['message']        = data['error']['message']
            return ouput
        else:
            ouput['return_code']    = 200
            ouput['values']         = data['values']
            return ouput

    def get_devices(self):
        ouput = {}
        ouput['mobiledevices']  = []
        initial_request = 'https://www.googleapis.com/admin/directory/v1/customer/C02bgpnb8/devices/mobile?orderBy=email&projection=BASIC'
        request = 'https://www.googleapis.com/admin/directory/v1/customer/C02bgpnb8/devices/mobile?orderBy=email&projection=BASIC'
        has_next_page = True
        while has_next_page :
            try:
                response = self.session.request('GET', request)
            except RefreshError as e:
                ouput['return_code']    = 500
                ouput['message']        = str(e)
                return ouput
            result = vars(response)
            data = json.loads(result['_content'])
            if 'error' in data:
                ouput['return_code']    = data['error']['code']
                ouput['message']        = data['error']['message']
                return ouput
            else:
                ouput['return_code']    = 200
                ouput['mobiledevices']  = ouput['mobiledevices'] + data['mobiledevices']
            if not 'nextPageToken' in data:
                has_next_page = False
            else:
                # print("Next Page Token: " + data['nextPageToken'])
                request = initial_request + "&pageToken=" + data['nextPageToken']
        return ouput
        








        