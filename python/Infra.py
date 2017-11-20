import os
import subprocess
import smtplib
import requests, bs4

from smtplib import SMTPException
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from EmailNotification import EmailNotification

# __all__ = ['tail']

def tail(f, n=10):
    if os.path.isfile(f):
        p = subprocess.Popen(['tail', '-n', str(n), f], stdout=subprocess.PIPE)
        lines = p.communicate()[0].split("\n")
        lines.reverse()
        # logging.debug(lines)
        return lines
    else:
        logging.error("Could not read file " + f)
        return 0

def loadDict(f):
    s = open(f, 'r').read()
    adict = eval(s)
    return adict

def saveDict(f, adict):
    target = open(f, 'w')
    target.write(str(adict))

def notify(sender, receiver, message = "Please ignore this email", subject = "Testing, please ignore", mail_server = 'mail.denagames-asia.local'):
    header = "From: "+ sender +"""
To: """ + receiver + """
MIME-Version: 1.0
Content-type: text/html
Subject: """ + subject + """

""";
    full_message = header + message
    try:
        smtpObj = smtplib.SMTP(mail_server)
        smtpObj.sendmail(sender, receivers, full_message)         
        logging.info("Successfully sent email")
    except SMTPException:
        logging.error("Unable to send email")

def tar(dir_name):
    try:
        subprocess.check_call(['tar', '-zcf', dir_name + ".tar.gz", dir_name])
        subprocess.check_call(['rm', '-rf', dir_name])
    except subprocess.CalledProcessError:
        logging.error("Could not compress directory: "+ dir_name)

def myIp():
    response = requests.get('http://ipinfo.io/ip')
    ip = bs4.BeautifulSoup(response.text, 'html5lib').select('body')[0].getText().split()[0]
    return ip


def Gauth(scope, flags, client_secret_file = 'client_id.json', credential_file = 'credential.json', app_name='quyen.le@punch.vn'):

    """Authenticate with Google
    Before run this program you must: 
    - Create a project and its secret file (to generate credential file). 
    - Download json format of the secret file, save it to local directory, name it as client_secret_file variable(above)
    - Remember to delete this file after run.

    In the first time program is run (with a project), you must grant permission for
     the project on the Google permission request page.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, credential_file )
    if credential_file != 'credential.json':
        credential_path = credential_file;


    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        client_secret_path = os.path.join(credential_dir, client_secret_file);
        if client_secret_file != 'client_id.json':
            client_secret_path = client_secret_file
        flow = client.flow_from_clientsecrets(client_secret_path, scope)
        flow.user_agent = app_name
        # print('Storing credentials to ' + credential_path)
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
    return credentials

def pmail(email_list, template):
    """Prety mail"""
    e = EmailNotification("SENDMAIL", "Infra Hanoi", "infra@punch.vn", "infra@punch.vn")
    e.mailbulk(email_list, template)


# End 